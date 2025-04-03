#!/usr/bin/env python3
# Wordlist Generator for Ethical Password Testing
# Author: AI-F0rc3
# Description: Generates custom wordlists for authorized penetration testing

import os
import sys
import time
import logging
import argparse
import itertools
import requests
from typing import List, Dict, Any, Set
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wordlist_generator.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("wordlist_generator")

class WordlistGenerator:
    def __init__(self):
        self.wordlist: Set[str] = set()
        self.personal_info: Dict[str, str] = {}
        self.api_key: str = ""
        self.api_provider: str = "openai"  # Default to OpenAI
        self.api_base_url: str = ""  # Custom API base URL for some providers
        self.output_file: str = f"wordlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.min_password_length: int = 0  # Minimum password length (0 = no minimum)
        self.max_password_length: int = 0  # Maximum password length (0 = no maximum)
        
    def collect_personal_info(self) -> None:
        """Collect personal information from user input."""
        print("\n=== Personal Information Collection ===")
        print("Note: This data is used only for wordlist generation and is not stored or transmitted.")
        
        self.personal_info["first_name"] = input("First Name: ").strip()
        self.personal_info["middle_name"] = input("Middle Name (Enter to skip): ").strip()
        self.personal_info["last_name"] = input("Last Name: ").strip()
        self.personal_info["nickname"] = input("Nickname (Enter to skip): ").strip()
        self.personal_info["pet_name"] = input("Pet Name (Enter to skip): ").strip()
        self.personal_info["birth_year"] = input("Birth Year (YYYY) (Enter to skip): ").strip()
        
        # Additional information
        additional_words = input("Additional keywords (comma separated): ").strip()
        if additional_words:
            self.personal_info["additional_words"] = [word.strip() for word in additional_words.split(',')]
        else:
            self.personal_info["additional_words"] = []
            
        # Important dates
        important_dates = input("Important dates (DDMMYYYY, comma separated): ").strip()
        if important_dates:
            self.personal_info["important_dates"] = [date.strip() for date in important_dates.split(',')]
        else:
            self.personal_info["important_dates"] = []
            
        # Password length constraints
        try:
            min_length = input("Minimum password length (Enter to skip): ").strip()
            self.min_password_length = int(min_length) if min_length else 0
            
            max_length = input("Maximum password length (Enter to skip): ").strip()
            self.max_password_length = int(max_length) if max_length else 0
            
            # Validate password length constraints
            if self.min_password_length < 0:
                self.min_password_length = 0
                print("Minimum password length cannot be negative. Using no minimum length.")
                
            if self.max_password_length < 0:
                self.max_password_length = 0
                print("Maximum password length cannot be negative. Using no maximum length.")
                
            if self.min_password_length > 0 and self.max_password_length > 0 and self.min_password_length > self.max_password_length:
                print("Warning: Minimum length is greater than maximum length. Swapping values.")
                self.min_password_length, self.max_password_length = self.max_password_length, self.min_password_length
                
        except ValueError:
            print("Invalid password length. Using no length constraints.")
            self.min_password_length = 0
            self.max_password_length = 0
    
    def filter_by_length(self, variations: List[str]) -> List[str]:
        """Filter password variations by length constraints."""
        if self.min_password_length <= 0 and self.max_password_length <= 0:
            return variations
            
        filtered_variations = []
        for password in variations:
            length = len(password)
            
            # Apply minimum length filter if set
            if self.min_password_length > 0 and length < self.min_password_length:
                continue
                
            # Apply maximum length filter if set
            if self.max_password_length > 0 and length > self.max_password_length:
                continue
                
            filtered_variations.append(password)
            
        logger.info(f"Filtered passwords by length constraints: {len(variations)} -> {len(filtered_variations)}")
        return filtered_variations
    
    def generate_basic_variations(self) -> None:
        """Generate basic variations from personal information."""
        logger.info("Generating basic variations...")
        
        # Add original values
        for key, value in self.personal_info.items():
            if isinstance(value, str) and value:
                self.wordlist.add(value.lower())
                self.wordlist.add(value.capitalize())
                
                # Special cases for names
                if key in ["first_name", "middle_name", "last_name", "nickname", "pet_name"]:
                    self.wordlist.add(value.upper())
                    
                    # First character capitalized
                    if len(value) > 1:
                        self.wordlist.add(value[0].upper() + value[1:].lower())
        
        # Add list values
        for key in ["additional_words", "important_dates"]:
            if key in self.personal_info:
                for item in self.personal_info[key]:
                    self.wordlist.add(item.lower())
                    self.wordlist.add(item.capitalize())
        
        # Generate combinations
        name_components = []
        for key in ["first_name", "middle_name", "last_name", "nickname"]:
            if key in self.personal_info and self.personal_info[key]:
                name_components.append(self.personal_info[key].lower())
                name_components.append(self.personal_info[key].capitalize())
        
        # Generate combinations of 2 name components
        for combo in itertools.permutations(name_components, 2):
            self.wordlist.add(combo[0] + combo[1])
            self.wordlist.add(f"{combo[0]}_{combo[1]}")
            self.wordlist.add(f"{combo[0]}.{combo[1]}")
            
        # Add year variations
        if "birth_year" in self.personal_info and self.personal_info["birth_year"]:
            year = self.personal_info["birth_year"]
            
            # Add just the year
            self.wordlist.add(year)
            
            # Add year at the end of names
            for name in name_components:
                self.wordlist.add(f"{name}{year}")
                self.wordlist.add(f"{name}_{year}")
                self.wordlist.add(f"{name}{year[-2:]}")
        
        # Add common number patterns
        common_numbers = ["123", "1234", "12345", "123456", "654321", "0123", "1111", "2222"]
        for name in name_components:
            for num in common_numbers:
                self.wordlist.add(f"{name}{num}")
                
        # Add common special character patterns
        special_chars = ["!", "@", "#", "$", "%", "&", "*"]
        for name in name_components:
            for char in special_chars:
                self.wordlist.add(f"{name}{char}")
                self.wordlist.add(f"{char}{name}")
                self.wordlist.add(f"{name}{char}{year[-2:]}" if "birth_year" in self.personal_info and self.personal_info["birth_year"] else "")
        
        logger.info(f"Generated {len(self.wordlist)} basic variations.")
        
        # Apply length filters if set
        if self.min_password_length > 0 or self.max_password_length > 0:
            original_wordlist = self.wordlist.copy()
            self.wordlist = set(self.filter_by_length(list(self.wordlist)))
            logger.info(f"Applied length filtering: {len(original_wordlist)} -> {len(self.wordlist)} variations")
    
    def generate_ai_variations(self) -> None:
        """Generate creative variations using AI API."""
        if not self.api_key:
            logger.warning("No API key provided. Skipping AI-powered variations.")
            return
            
        logger.info(f"Generating AI-powered variations using {self.api_provider}...")
        
        # Create a prompt for the AI with personal information
        prompt = f"""
        Generate a list of 20 creative password variations based on the following information.
        Only output the passwords, one per line, with no additional text or explanation:
        
        First name: {self.personal_info.get('first_name', '')}
        Middle name: {self.personal_info.get('middle_name', '')}
        Last name: {self.personal_info.get('last_name', '')}
        Nickname: {self.personal_info.get('nickname', '')}
        Pet name: {self.personal_info.get('pet_name', '')}
        Birth year: {self.personal_info.get('birth_year', '')}
        Additional words: {', '.join(self.personal_info.get('additional_words', []))}
        Important dates: {', '.join(self.personal_info.get('important_dates', []))}
        """
        
        # Add length constraints if specified
        if self.min_password_length > 0:
            prompt += f"\nMinimum password length: {self.min_password_length} characters"
        
        if self.max_password_length > 0:
            prompt += f"\nMaximum password length: {self.max_password_length} characters"
            
        prompt += """
        
        Generate passwords that combine this information with common patterns,
        special characters, substitutions, and numbers. Focus on realistic combinations
        that people might actually use.
        """
        
        try:
            variations = []
            
            if self.api_provider == "openai":
                variations = self._generate_with_openai(prompt)
            elif self.api_provider == "gemini":
                variations = self._generate_with_gemini(prompt)
            elif self.api_provider == "grok":
                variations = self._generate_with_grok(prompt)
            elif self.api_provider == "deepseek":
                variations = self._generate_with_deepseek(prompt)
            elif self.api_provider == "llama3":
                variations = self._generate_with_llama3(prompt)
            else:
                logger.error(f"Unknown API provider: {self.api_provider}")
                return
                
            # Filter by length if constraints are set
            if self.min_password_length > 0 or self.max_password_length > 0:
                variations = self.filter_by_length(variations)
                
            # Add the AI-generated variations to the wordlist
            for variation in variations:
                variation = variation.strip()
                if variation:
                    self.wordlist.add(variation)
            
            logger.info(f"Added {len(variations)} AI-generated variations.")
            
        except Exception as e:
            logger.error(f"Unexpected error during AI variation generation: {str(e)}")
    
    def _generate_with_openai(self, prompt: str) -> List[str]:
        """Generate variations using OpenAI API."""
        try:
            # Configure API request for OpenAI
            api_url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"].strip().split("\n")
            else:
                logger.warning("OpenAI API returned an unexpected response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return []
    
    def _generate_with_gemini(self, prompt: str) -> List[str]:
        """Generate variations using Google's Gemini API."""
        try:
            # Configure API request for Gemini
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 500
                }
            }
            
            # Make the API request
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "candidates" in result and result["candidates"]:
                text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                return text_content.strip().split("\n")
            else:
                logger.warning("Gemini API returned an unexpected response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return []
    
    def _generate_with_grok(self, prompt: str) -> List[str]:
        """Generate variations using Grok API."""
        try:
            # Configure API request for Grok
            api_url = "https://api.grok.ai/v1/chat/completions"
            if self.api_base_url:
                api_url = f"{self.api_base_url}/v1/chat/completions"
                
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "grok-1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"].strip().split("\n")
            else:
                logger.warning("Grok API returned an unexpected response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Grok API: {str(e)}")
            return []
    
    def _generate_with_deepseek(self, prompt: str) -> List[str]:
        """Generate variations using DeepSeek R1 API."""
        try:
            # Configure API request for DeepSeek
            api_url = "https://api.deepseek.com/v1/chat/completions"
            if self.api_base_url:
                api_url = f"{self.api_base_url}/v1/chat/completions"
                
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "deepseek-r1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"].strip().split("\n")
            else:
                logger.warning("DeepSeek API returned an unexpected response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            return []
    
    def _generate_with_llama3(self, prompt: str) -> List[str]:
        """Generate variations using Llama 3 API."""
        try:
            # Configure API request for Llama 3
            api_url = "https://api.llama.ai/v1/chat/completions"
            if self.api_base_url:
                api_url = f"{self.api_base_url}/v1/chat/completions"
                
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "llama-3",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"].strip().split("\n")
            else:
                logger.warning("Llama 3 API returned an unexpected response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Llama 3 API: {str(e)}")
            return []
    
    def save_wordlist(self) -> None:
        """Save the generated wordlist to a file."""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for word in sorted(self.wordlist):
                    f.write(f"{word}\n")
            
            logger.info(f"Wordlist saved to {self.output_file} with {len(self.wordlist)} entries.")
            print(f"\nWordlist saved to: {self.output_file}")
            print(f"Total passwords generated: {len(self.wordlist)}")
        except Exception as e:
            logger.error(f"Error saving wordlist: {str(e)}")
            print(f"Error saving wordlist: {str(e)}")
    
    def prepare_for_hydra(self, target: str, service: str) -> str:
        """
        Prepare a Hydra command for brute-force testing.
        
        Args:
            target: The target IP or hostname
            service: The service to attack (ssh, ftp, http-post-form, etc.)
            
        Returns:
            str: The prepared Hydra command
        """
        if not os.path.exists(self.output_file):
            logger.error("Wordlist file not found. Generate wordlist first.")
            return ""
        
        # Construct username list from personal info
        username_file = "usernames.txt"
        usernames = []
        
        if self.personal_info.get("first_name"):
            usernames.append(self.personal_info["first_name"].lower())
        
        if self.personal_info.get("last_name"):
            usernames.append(self.personal_info["last_name"].lower())
            
        if self.personal_info.get("first_name") and self.personal_info.get("last_name"):
            usernames.append(f"{self.personal_info['first_name'].lower()}.{self.personal_info['last_name'].lower()}")
            usernames.append(f"{self.personal_info['first_name'][0].lower()}{self.personal_info['last_name'].lower()}")
            
        if self.personal_info.get("nickname"):
            usernames.append(self.personal_info["nickname"].lower())
        
        try:
            with open(username_file, 'w', encoding='utf-8') as f:
                for username in set(usernames):
                    f.write(f"{username}\n")
            
            logger.info(f"Username list saved to {username_file} with {len(set(usernames))} entries.")
        except Exception as e:
            logger.error(f"Error saving username list: {str(e)}")
            return ""
        
        # Construct the Hydra command
        hydra_cmd = f"hydra -L {username_file} -P {self.output_file} {target} {service}"
        
        if service == "http-post-form":
            hydra_cmd += "'/login.php:username=^USER^&password=^PASS^:Invalid credentials'"
        
        hydra_cmd += " -t 4 -V"
        
        logger.info(f"Prepared Hydra command: {hydra_cmd}")
        return hydra_cmd
    
    def show_options_help(self) -> None:
        """Display detailed help information about command-line options."""
        help_text = """
Ethical Password Wordlist Generator - Command Options Help
=========================================================

GENERAL OPTIONS:
---------------
--help                      Show the basic help message
--show-functions            List all available functions
--help-function NAME        Show detailed help for a specific function
--help-options              Show this detailed command options help

WORDLIST GENERATION OPTIONS:
---------------------------
--output FILE               Specify a custom output filename for the wordlist
                            Example: --output my_passwords.txt
                            Default: wordlist_YYYYMMDD_HHMMSS.txt

--min-length NUM            Specify minimum password length
                            Example: --min-length 8
                            Default: No minimum length

--max-length NUM            Specify maximum password length
                            Example: --max-length 16
                            Default: No maximum length

AI INTEGRATION OPTIONS:
---------------------
--use-ai                    Enable AI-powered password variations
                            Requires: --api-key

--api-key KEY               Specify the API key for AI integration
                            Example: --api-key sk_1234567890abcdef
                            Required if --use-ai is specified

--api-provider PROVIDER     Choose which AI provider to use
                            Options: openai, gemini, grok, deepseek, llama3
                            Example: --api-provider gemini
                            Default: openai

--api-base-url URL          Custom API base URL for self-hosted models
                            Example: --api-base-url http://localhost:8000
                            Default: Provider's official API endpoint

EXAMPLES:
--------
1. Basic usage (interactive mode):
   python wordlist_generator.py

2. Using OpenAI with custom output file:
   python wordlist_generator.py --use-ai --api-key YOUR_API_KEY --output passwords.txt

3. Using Gemini with password length constraints:
   python wordlist_generator.py --use-ai --api-key YOUR_API_KEY --api-provider gemini --min-length 8 --max-length 16

4. Using a self-hosted model:
   python wordlist_generator.py --use-ai --api-key YOUR_API_KEY --api-provider llama3 --api-base-url http://localhost:8000

5. Getting help for a specific function:
   python wordlist_generator.py --help-function generate_ai_variations

NOTES:
-----
- All personal information is collected interactively and is not stored or transmitted
- The tool is designed for ethical security testing ONLY
- Use only on systems you own or have explicit permission to test
- The password length constraints apply to both basic and AI-generated variations
"""
        print(help_text)
    
    def show_help(self, function_name: str = "") -> None:
        """Display help information about available functions.
        
        Args:
            function_name: Optional specific function to get help for. If empty, shows all functions.
        """
        help_info = {
            "general": """
Ethical Password Wordlist Generator - Help
==========================================
This tool generates custom wordlists for password testing based on personal information
and can use AI to create more sophisticated variations.

Basic usage:
    python wordlist_generator.py
    
With AI integration:
    python wordlist_generator.py --use-ai --api-key YOUR_API_KEY

Available commands:
    --help                      Show this help message
    --show-functions            Show available functions and their descriptions
    
For more detailed help on a specific function, use:
    python wordlist_generator.py --help-function FUNCTION_NAME
    
Example:
    python wordlist_generator.py --help-function generate_ai_variations
""",
            "collect_personal_info": """
Function: collect_personal_info()
================================
Collects personal information from user input that will be used to generate password variations.

Information collected:
- First name
- Middle name
- Last name
- Nickname
- Pet name
- Birth year
- Additional keywords
- Important dates
- Password length constraints (minimum and maximum)

The information is stored in the personal_info dictionary and used by other functions.
This data is only used locally for wordlist generation and is not transmitted or stored.
""",
            "generate_basic_variations": """
Function: generate_basic_variations()
===================================
Generates basic password variations using the collected personal information.

Types of variations created:
- Original values (lowercase, uppercase, capitalized)
- Combinations of name components
- Year variations (full year, last two digits)
- Common number patterns (123, 1234, etc.)
- Common special character patterns

The generated passwords are stored in the wordlist set.
If length constraints are set, the variations that don't meet these constraints will be filtered out.
""",
            "generate_ai_variations": """
Function: generate_ai_variations()
================================
Generates creative password variations using AI integration via API calls.

Requirements:
- An API key for the selected provider
- Internet connection to access the API

Supported AI providers:
- OpenAI (GPT-3.5 Turbo)
- Google Gemini Pro
- Grok
- DeepSeek R1
- Llama 3

The function creates a prompt with the personal information and sends it to the selected AI API.
The AI generates password variations that are then added to the wordlist.
If length constraints are set, only passwords meeting these requirements will be included.
""",
            "filter_by_length": """
Function: filter_by_length(variations)
====================================
Filters a list of password variations based on length constraints.

Parameters:
- variations: List of password strings to filter

Returns:
- Filtered list of passwords that meet the length constraints

The function applies both minimum and maximum length filters if they are set.
If no length constraints are set (both values are 0), it returns the original list unchanged.
""",
            "save_wordlist": """
Function: save_wordlist()
=======================
Saves the generated wordlist to a text file.

The wordlist is saved to the file specified by the output_file attribute.
If no custom filename was provided, it uses the default format:
    wordlist_YYYYMMDD_HHMMSS.txt

Each password is written on a separate line, sorted alphabetically.
The function also logs the number of passwords saved and displays this information to the user.
""",
            "prepare_for_hydra": """
Function: prepare_for_hydra(target, service)
==========================================
Prepares a Hydra command for password brute-force testing.

Parameters:
- target: The target IP or hostname
- service: The service to attack (ssh, ftp, http-post-form, smb)

Returns:
- A complete Hydra command string ready for execution

The function:
1. Creates a username file based on the collected personal information
2. Constructs a Hydra command using the wordlist and username file
3. Configures service-specific parameters (like form fields for HTTP)
4. Adds general Hydra options like thread count and verbosity

Important: Only use this against systems you own or have explicit permission to test!
""",
            "run": """
Function: run(use_ai, api_key, api_provider, api_base_url, output_file, min_length, max_length)
============================================================================================
Main function that orchestrates the wordlist generation process.

Parameters:
- use_ai: Whether to use AI for additional variations
- api_key: API key for the selected AI provider
- api_provider: Which AI provider to use
- api_base_url: Optional custom API endpoint
- output_file: Custom output filename
- min_length: Minimum password length
- max_length: Maximum password length

The function:
1. Sets up the configuration based on parameters
2. Collects personal information
3. Generates basic variations
4. Generates AI variations (if requested)
5. Saves the wordlist
6. Offers to prepare a Hydra command
"""
        }
        
        # If no specific function is requested, show general help
        if not function_name or function_name.lower() == "general":
            print(help_info["general"])
            return
            
        # If the user wants to see all available functions
        if function_name.lower() == "all" or function_name.lower() == "list":
            print("\nAvailable Functions:\n" + "="*20)
            for func in help_info:
                if func != "general":
                    # Extract just the first line of each function's help
                    first_line = help_info[func].strip().split("\n")[0]
                    print(f"- {first_line}")
            print("\nUse --help-function NAME to see detailed help for a specific function.")
            return
        
        # Show help for specific function
        function_name = function_name.lower()
        if function_name in help_info:
            print(help_info[function_name])
        else:
            print(f"Error: Function '{function_name}' not found.")
            print("\nAvailable functions:")
            for func in help_info:
                if func != "general":
                    print(f"- {func}")
    
    def run(self, use_ai: bool = False, api_key: str = "", api_provider: str = "openai", 
            api_base_url: str = "", output_file: str = "", 
            min_length: int = 0, max_length: int = 0,
            help_function: str = "") -> None:
        """Run the wordlist generation process."""
        
        # If help is requested, show help and return
        if help_function:
            self.show_help(help_function)
            return
        
        print("\n===== Ethical Password Wordlist Generator =====")
        print("DISCLAIMER: This tool is designed for ethical security testing ONLY.")
        print("Use only on systems you own or have explicit permission to test.")
        print("Unauthorized password attacks are illegal and unethical.")
        
        if output_file:
            self.output_file = output_file
        
        if use_ai:
            self.api_key = api_key
            if api_provider in ["openai", "gemini", "grok", "deepseek", "llama3"]:
                self.api_provider = api_provider
            else:
                logger.warning(f"Unknown API provider '{api_provider}'. Using OpenAI as default.")
            
            # Set custom API base URL if provided
            if api_base_url:
                self.api_base_url = api_base_url
                logger.info(f"Using custom API base URL: {api_base_url}")
        
        # Set password length constraints if provided via command line
        if min_length > 0:
            self.min_password_length = min_length
            logger.info(f"Using minimum password length: {min_length}")
            
        if max_length > 0:
            self.max_password_length = max_length
            logger.info(f"Using maximum password length: {max_length}")
            
        # Validate password length constraints
        if self.min_password_length > 0 and self.max_password_length > 0 and self.min_password_length > self.max_password_length:
            logger.warning("Minimum length is greater than maximum length. Swapping values.")
            self.min_password_length, self.max_password_length = self.max_password_length, self.min_password_length
        
        # Collect information
        self.collect_personal_info()
        
        # Generate variations
        self.generate_basic_variations()
        
        # Generate AI variations if requested
        if use_ai:
            self.generate_ai_variations()
        
        # Save wordlist
        self.save_wordlist()
        
        # Ask if user wants to prepare a Hydra command
        prepare_hydra = input("\nPrepare Hydra command for testing? (y/n): ").strip().lower()
        if prepare_hydra == 'y':
            target = input("Target IP/hostname: ").strip()
            print("\nAvailable services:")
            print("1. SSH")
            print("2. FTP")
            print("3. HTTP Post Form")
            print("4. SMB")
            service_choice = input("Select service (1-4): ").strip()
            
            service_map = {
                "1": "ssh",
                "2": "ftp",
                "3": "http-post-form",
                "4": "smb"
            }
            
            if service_choice in service_map:
                service = service_map[service_choice]
                hydra_cmd = self.prepare_for_hydra(target, service)
                
                if hydra_cmd:
                    print("\nPrepared Hydra command:")
                    print(hydra_cmd)
                    print("\nNOTE: Ensure you have legal authorization before executing this command.")
            else:
                print("Invalid service selection.")

def main():
    """Main function to parse arguments and run the wordlist generator."""
    parser = argparse.ArgumentParser(description="Ethical Password Wordlist Generator")
    parser.add_argument("--use-ai", action="store_true", help="Use AI to generate additional variations")
    parser.add_argument("--api-key", type=str, help="API key for AI integration")
    parser.add_argument("--api-provider", type=str, 
                       choices=["openai", "gemini", "grok", "deepseek", "llama3"], 
                       default="openai", 
                       help="AI provider to use")
    parser.add_argument("--api-base-url", type=str, help="Custom API base URL (for self-hosted or alternative endpoints)")
    parser.add_argument("--output", type=str, help="Output file name")
    parser.add_argument("--min-length", type=int, default=0, help="Minimum password length")
    parser.add_argument("--max-length", type=int, default=0, help="Maximum password length")
    parser.add_argument("--help-function", type=str, help="Show help for a specific function")
    parser.add_argument("--show-functions", action="store_true", help="Show list of all available functions")
    parser.add_argument("--help-options", action="store_true", help="Show detailed help for command-line options")
    
    args = parser.parse_args()
    
    generator = WordlistGenerator()
    
    # Handle help requests
    if args.help_options:
        generator.show_options_help()
        return
        
    if args.help_function:
        generator.show_help(args.help_function)
        return
        
    if args.show_functions:
        generator.show_help("all")
        return
    
    generator.run(
        use_ai=args.use_ai,
        api_key=args.api_key,
        api_provider=args.api_provider,
        api_base_url=args.api_base_url,
        output_file=args.output,
        min_length=args.min_length,
        max_length=args.max_length
    )

if __name__ == "__main__":
    main() 