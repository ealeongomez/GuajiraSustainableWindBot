"""
Security Module - Prompt Injection Protection and Query Validation
"""

import re
from typing import Tuple, List
from colorama import Fore, Style


class SecurityValidator:
    """Validates queries to prevent prompt injection and off-topic questions."""
    
    # Patrones de prompt injection comunes
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|above|prior)\s+instructions?",
        r"forget\s+(everything|all|previous)",
        r"you\s+are\s+now",
        r"new\s+instructions?",
        r"system\s+prompt",
        r"roleplay\s+as",
        r"pretend\s+(you|to)\s+are",
        r"disregard\s+(previous|all|above)",
        r"override\s+instructions?",
        r"\[SYSTEM\]",
        r"\[ADMIN\]",
        r"\[ROOT\]",
        r"</s>",
        r"<\|endoftext\|>",
        r"<\|im_end\|>",
    ]
    
    # Keywords fuera del dominio de La Guajira
    OFF_TOPIC_KEYWORDS = [
        # Otros lugares
        r"\b(bogot[aá]|medell[ií]n|cali|barranquilla|cartagena)\b",
        r"\b(espa[ñn]a|argentina|m[ée]xico|estados unidos|usa)\b",
        r"\b(europa|asia|[áa]frica)\b",
        
        # Temas no relacionados
        r"\b(futbol|soccer|basketball|deportes)\b",
        r"\b(pol[ií]tica|elecciones|gobierno)\b",
        r"\b(m[úu]sica|pel[ií]culas|cine|entretenimiento)\b",
        r"\b(comida|recetas|cocina)\b",
        r"\b(cripto|bitcoin|acciones|bolsa)\b",
    ]
    
    # Keywords válidos de La Guajira
    VALID_KEYWORDS = [
        # Municipios
        r"\b(albania|barrancas|distracci[óo]n|el molino|fonseca)\b",
        r"\b(hatonuevo|la jagua|maicao|manaure|mingueo)\b",
        r"\b(riohacha|san juan|uribia)\b",
        
        # Términos técnicos válidos
        r"\b(viento|wind|velocidad|speed)\b",
        r"\b(temperatura|temperature|humedad|humidity)\b",
        r"\b(energ[ií]a|energy|e[óo]lica|sostenible|sustainable)\b",
        r"\b(lstm|modelo|predicci[óo]n|forecast)\b",
        r"\b(municipio|guajira|colombia)\b",
        r"\b(gr[áa]fica|plot|visualizaci[óo]n)\b",
        r"\b(promedio|average|m[áa]ximo|maximum|m[ií]nimo|minimum)\b",
        r"\b(datos|data|an[áa]lisis|estad[ií]stica)\b",
    ]
    
    def __init__(self, verbose: bool = False):
        """
        Initialize Security Validator.
        
        Args:
            verbose: Whether to print validation messages
        """
        self.verbose = verbose
        
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate a user query for security and relevance.
        
        Args:
            query: User's query string
            
        Returns:
            Tuple of (is_valid, reason)
        """
        query_lower = query.lower()
        
        # 1. Check for prompt injection attempts
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, query_lower, re.IGNORECASE):
                if self.verbose:
                    print(f"{Fore.RED}⚠️  Prompt injection detectado{Style.RESET_ALL}")
                return False, "Consulta inválida: intento de manipulación detectado."
        
        # 2. Check for code injection in query
        code_patterns = [
            r"import\s+\w+",
            r"exec\s*\(",
            r"eval\s*\(",
            r"__import__",
            r"subprocess",
            r"os\.system",
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, query_lower):
                if self.verbose:
                    print(f"{Fore.RED}⚠️  Inyección de código detectada{Style.RESET_ALL}")
                return False, "Consulta inválida: intento de inyección de código."
        
        # 3. Check if query is too short or too long
        if len(query.strip()) < 3:
            return False, "Consulta muy corta. Por favor, sea más específico."
        
        if len(query) > 500:
            return False, "Consulta muy larga. Por favor, sea más conciso."
        
        # 4. Check for off-topic keywords
        for pattern in self.OFF_TOPIC_KEYWORDS:
            if re.search(pattern, query_lower, re.IGNORECASE):
                if self.verbose:
                    print(f"{Fore.YELLOW}⚠️  Tema fuera del dominio detectado{Style.RESET_ALL}")
                return False, "Esta consulta está fuera del dominio. Solo puedo responder sobre viento y energía en La Guajira, Colombia."
        
        # 5. Check if query is related to La Guajira domain
        # Si la consulta es muy corta, puede ser general (permitir)
        if len(query.strip()) < 15:
            return True, "ok"
        
        # Para consultas más largas, verificar que contenga keywords válidos
        has_valid_keyword = False
        for pattern in self.VALID_KEYWORDS:
            if re.search(pattern, query_lower, re.IGNORECASE):
                has_valid_keyword = True
                break
        
        # Si no tiene keywords válidos pero no tiene off-topic, verificar si es pregunta conceptual
        if not has_valid_keyword:
            # Verificar si es una pregunta conceptual o general sobre el sistema
            conceptual_keywords = [
                r"\b(qu[ée]|c[óo]mo|por qu[ée]|explica|define|cu[aá]ntos|cu[aá]l)\b",
                r"\b(modelo|predicci[óo]n|energ[ií]a|viento|municipio|sistema|bot)\b",
            ]
            
            is_conceptual = any(re.search(p, query_lower, re.IGNORECASE) 
                              for p in conceptual_keywords)
            
            if is_conceptual:
                return True, "ok"
            
            # Si no es conceptual ni tiene keywords, podría ser off-topic
            if self.verbose:
                print(f"{Fore.YELLOW}⚠️  Consulta posiblemente fuera de dominio{Style.RESET_ALL}")
            return False, "Esta consulta parece estar fuera del dominio. Solo puedo responder sobre predicción de viento y energía en La Guajira, Colombia."
        
        return True, "ok"
    
    def sanitize_code(self, code: str) -> str:
        """
        Sanitize generated code to prevent malicious operations.
        
        Args:
            code: Generated Python code
            
        Returns:
            Sanitized code or empty string if unsafe
        """
        # Lista negra de operaciones peligrosas
        forbidden_operations = [
            'import os',
            'import sys',
            'import subprocess',
            '__import__',
            'exec(',
            'eval(',
            'compile(',
            'open(',
            'file(',
            'input(',
            'raw_input(',
            'reload(',
        ]
        
        code_lower = code.lower()
        
        for forbidden in forbidden_operations:
            if forbidden.lower() in code_lower:
                if self.verbose:
                    print(f"{Fore.RED}⚠️  Código malicioso detectado: {forbidden}{Style.RESET_ALL}")
                return ""
        
        return code


def validate_and_sanitize(query: str, verbose: bool = False) -> Tuple[bool, str]:
    """
    Convenience function to validate a query.
    
    Args:
        query: User's query
        verbose: Whether to print messages
        
    Returns:
        Tuple of (is_valid, reason)
    """
    validator = SecurityValidator(verbose=verbose)
    return validator.validate_query(query)

