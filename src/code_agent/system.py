"""
Multi-Agent System - Orchestrates all agents
"""

from typing import Dict
from colorama import Fore, Style

from .config import MUNICIPALITIES, get_supervisor_llm, get_agent_llm
from .data_manager import DataManager
from .supervisor import SupervisorAgent
from .municipality_agent import CodeMunicipalityAgent
from .general_agent import GeneralAgent


class CodeMultiAgentSystem:
    """Orchestrates the supervisor and code-enabled agents."""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Multi-Agent System.
        
        Args:
            verbose: Whether to print initialization messages
        """
        self.verbose = verbose
        
        # Initialize data manager
        self.data_manager = DataManager(verbose=verbose)
        
        # Initialize LLMs
        if verbose:
            print(f"{Fore.GREEN}✅ Modelos LLM inicializados (GPT-4){Style.RESET_ALL}\n")
        
        supervisor_llm = get_supervisor_llm()
        agent_llm = get_agent_llm()
        
        # Initialize agents
        self.supervisor = SupervisorAgent(supervisor_llm)
        self.general_agent = GeneralAgent(agent_llm)
        self.municipality_agents: Dict[str, CodeMunicipalityAgent] = {}
        
        # Initialize municipality agents
        if verbose:
            print(f"{Fore.YELLOW}🤖 Inicializando agentes municipales...{Style.RESET_ALL}")
        
        for municipality in MUNICIPALITIES:
            self.municipality_agents[municipality] = CodeMunicipalityAgent(
                municipality, 
                agent_llm,
                self.data_manager
            )
        
        if verbose:
            print(f"{Fore.GREEN}✅ Sistema multi-agente listo ({len(MUNICIPALITIES)} agentes){Style.RESET_ALL}\n")
    
    def process_query(self, query: str, verbose: bool = None) -> str:
        """
        Process user query through the multi-agent system.
        
        Args:
            query: User's question
            verbose: Override instance verbose setting
            
        Returns:
            Response string
        """
        if verbose is None:
            verbose = self.verbose
        
        # Step 1: Supervisor routes the query
        if verbose:
            print(f"{Fore.YELLOW}🔍 Supervisor analizando consulta...{Style.RESET_ALL}")
        
        routing = self.supervisor.route_query(query)
        
        if verbose:
            print(f"{Fore.CYAN}📋 Tipo: {routing['type']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📍 Municipios: {routing['municipalities'] if routing['municipalities'] else 'ninguno'}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🐍 Necesita código: {'Sí' if routing['needs_code'] else 'No'}{Style.RESET_ALL}\n")
        
        # Step 2: Route to appropriate agent(s)
        if routing["type"] == "general":
            if verbose:
                print(f"{Fore.MAGENTA}🌐 Enrutando a agente general...{Style.RESET_ALL}\n")
            return self.general_agent.answer(query)
        
        elif routing["municipalities"]:
            if len(routing["municipalities"]) == 1:
                municipality = routing["municipalities"][0]
                if verbose:
                    print(f"{Fore.MAGENTA}📊 Enrutando a agente de {municipality.replace('_', ' ').title()}...{Style.RESET_ALL}\n")
                
                if municipality in self.municipality_agents:
                    return self.municipality_agents[municipality].answer(query)
                else:
                    return f"Municipio '{municipality}' no encontrado."
            
            else:
                # Multiple municipalities - aggregate responses
                if verbose:
                    print(f"{Fore.MAGENTA}📊 Consultando múltiples municipios...{Style.RESET_ALL}\n")
                
                responses = []
                for municipality in routing["municipalities"]:
                    if municipality in self.municipality_agents:
                        if verbose:
                            print(f"{Fore.CYAN}  → {municipality.replace('_', ' ').title()}{Style.RESET_ALL}")
                        response = self.municipality_agents[municipality].answer(query)
                        responses.append(f"\n**{municipality.replace('_', ' ').title()}:**\n{response}")
                
                return "\n".join(responses) if responses else "No se encontraron municipios válidos."
        
        else:
            # Fallback to general
            return self.general_agent.answer(query)

