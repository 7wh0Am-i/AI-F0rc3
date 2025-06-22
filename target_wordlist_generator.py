#!/usr/bin/env python3
# Target-based Wordlist Generator for Ethical Password Testing
# Author: 7wh0Am-i (https://github.com/7wh0Am-i)
# Description: Generates custom wordlists based on target information

import os
import sys
import time
import logging
import pyfiglet
from typing import List, Dict, Any, Set
from datetime import datetime
import itertools
import random
import string

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wordlist_generator.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("target_wordlist_generator")

class TargetWordlistGenerator:
    def __init__(self):
        self.wordlist: Set[str] = set()
        self.target_info: Dict[str, Any] = {}
        self.output_file: str = f"target_wordlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.min_password_length: int = 8  # Default minimum password length
        self.max_password_length: int = 16  # Default maximum password length
        self.password_count: int = 100  # Default number of passwords to generate
        self.common_suffixes = ["123", "1234", "321", "!", "#", "@", "2023", "2024", "2025", "123!"]
        self.common_prefixes = ["The", "My", "A", "Secret", "Super"]
        
    def collect_target_info(self) -> None:
        """Collect information about the target from user input."""
        print("\nWARNING: Only use this tool for ethical and legal password testing.")
        print("Using this tool without authorization is illegal and unethical.")
        print("\n=== Target Information Collection ===")
        print("Enter information about your target to create a customized wordlist.")
        
        # Get password count and length requirements
        try:
            count_input = input("\nHow many passwords do you need? (default: 100): ").strip()
            self.password_count = int(count_input) if count_input else 100
            
            min_len_input = input("Minimum password length? (default: 8): ").strip()
            self.min_password_length = int(min_len_input) if min_len_input else 8
            
            max_len_input = input("Maximum password length? (default: 16): ").strip()
            self.max_password_length = int(max_len_input) if max_len_input else 16
            
            # Validate inputs
            if self.password_count < 1:
                self.password_count = 100
                print("Password count must be at least 1. Using default: 100")
            
            if self.min_password_length < 1:
                self.min_password_length = 8
                print("Minimum length must be at least 1. Using default: 8")
                
            if self.max_password_length < self.min_password_length:
                self.max_password_length = max(16, self.min_password_length * 2)
                print(f"Maximum length must be >= minimum length. Using: {self.max_password_length}")
                
        except ValueError:
            print("Invalid numeric input. Using default values.")
            self.password_count = 100
            self.min_password_length = 8
            self.max_password_length = 16
        
        print("\n=== Target Personal Information ===")
        self.target_info["first_name"] = input("First Name: ").strip()
        self.target_info["last_name"] = input("Last Name: ").strip()
        self.target_info["nickname"] = input("Nickname/Username (Enter to skip): ").strip()
        self.target_info["birth_year"] = input("Birth Year (YYYY) (Enter to skip): ").strip()
        
        # Ask if the user wants to provide Company/Organization info
        include_company = input("\nInclude Company/Organization information? (y/n): ").strip().lower()
        if include_company == 'y':
            print("\n=== Company/Organization Information ===")
            self.target_info["company_name"] = input("Company/Organization Name: ").strip()
            self.target_info["company_short"] = input("Company Short Name/Abbreviation: ").strip()
            self.target_info["job_title"] = input("Job Title/Position: ").strip()
            self.target_info["department"] = input("Department: ").strip()
        
        # Ask if the user wants to provide additional information
        include_additional = input("\nInclude additional personal information? (y/n): ").strip().lower()
        if include_additional == 'y':
            print("\n=== Additional Information ===")
            pet_name = input("Pet Name (if known, Enter to skip): ").strip()
            if pet_name:
                self.target_info["pet_name"] = pet_name
                
            spouse_name = input("Spouse/Partner Name (if known, Enter to skip): ").strip()
            if spouse_name:
                self.target_info["spouse_name"] = spouse_name
                
            child_name = input("Child's Name (if known, Enter to skip): ").strip()
            if child_name:
                self.target_info["child_name"] = child_name
        
        # Ask if user wants to provide important dates
        include_dates = input("\nInclude important dates? (y/n): ").strip().lower()
        if include_dates == 'y':
            print("\n=== Important Dates ===")
            print("Enter dates in DDMMYYYY format (e.g., 15082023 for August 15, 2023)")
            
            birth_date = input("Birth Date (if known, Enter to skip): ").strip()
            if birth_date:
                self.target_info["birth_date"] = birth_date
                
            anniversary = input("Anniversary Date (if known, Enter to skip): ").strip()
            if anniversary:
                self.target_info["anniversary"] = anniversary
        
        # Interests and hobbies
        interests = input("\nInterests/Hobbies (comma separated, Enter to skip): ").strip()
        if interests:
            self.target_info["interests"] = [item.strip() for item in interests.split(',')]
        else:
            self.target_info["interests"] = []
            
        # Important keywords
        keywords = input("\nAdditional keywords (comma separated, Enter to skip): ").strip()
        if keywords:
            self.target_info["keywords"] = [word.strip() for word in keywords.split(',')]
        else:
            self.target_info["keywords"] = []
        
        print("\n=== Information Collection Complete ===")
        
    def filter_by_length(self, words: List[str]) -> List[str]:
        """Filter words by the specified length constraints."""
        return [word for word in words if self.min_password_length <= len(word) <= self.max_password_length]
    
    def generate_variations(self) -> None:
        """Generate password variations based on collected target information."""
        logger.info("Generating password variations...")
        
        # Initialize base words from target info
        base_words = []
        for key, value in self.target_info.items():
            if isinstance(value, str) and value:
                # Add the value in different forms
                base_words.append(value.lower())
                base_words.append(value.capitalize())
                
                # For names, company names and similar fields, add variants
                if key in ["first_name", "last_name", "nickname", "company_name", "company_short", "pet_name", "spouse_name", "child_name"]:
                    base_words.append(value.upper())
                    if len(value) > 1:
                        base_words.append(value[0].upper() + value[1:].lower())
        
        # Add items from lists
        for key in ["interests", "keywords"]:
            if key in self.target_info:
                for item in self.target_info[key]:
                    base_words.append(item.lower())
                    base_words.append(item.capitalize())
        
        # Generate name combinations
        name_components = []
        for key in ["first_name", "last_name", "nickname"]:
            if key in self.target_info and self.target_info[key]:
                name_components.append(self.target_info[key].lower())
                name_components.append(self.target_info[key].capitalize())
        
        # Name combinations
        for combo in itertools.product(name_components, repeat=2):
            if combo[0] != combo[1]:  # Avoid repeating the same component
                base_words.append(combo[0] + combo[1])
                base_words.append(f"{combo[0]}.{combo[1]}")
                base_words.append(f"{combo[0]}_{combo[1]}")
        
        # Work-related combinations
        work_components = []
        for key in ["company_name", "company_short", "job_title", "department"]:
            if key in self.target_info and self.target_info[key]:
                work_components.append(self.target_info[key].lower())
                work_components.append(self.target_info[key].capitalize())
        
        # Work combinations
        for name in name_components:
            for work in work_components:
                base_words.append(f"{name}{work}")
                base_words.append(f"{work}{name}")
        
        # Add date variations
        year_variations = []
        if "birth_year" in self.target_info and self.target_info["birth_year"]:
            year = self.target_info["birth_year"]
            year_variations += [year, year[-2:]]
            
            # Years around the birth year (people often use birth year +/- 1)
            try:
                birth_year_int = int(year)
                year_variations.append(str(birth_year_int + 1))
                year_variations.append(str(birth_year_int - 1))
            except ValueError:
                pass
        
        # Current year and recent years
        current_year = datetime.now().year
        for i in range(5):
            year_variations.append(str(current_year - i))
            year_variations.append(str(current_year - i)[-2:])
        
        # Add years to base words
        base_with_years = []
        for word in base_words:
            for year in year_variations:
                base_with_years.append(f"{word}{year}")
                base_with_years.append(f"{word}_{year}")
        
        base_words.extend(base_with_years)
        
        # Add common suffixes
        with_suffixes = []
        for word in base_words:
            for suffix in self.common_suffixes:
                with_suffixes.append(f"{word}{suffix}")
        
        base_words.extend(with_suffixes)
        
        # Common character replacements (leet speak)
        leet_replacements = {
            'a': ['@', '4'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['$', '5'],
            't': ['7'],
            'b': ['8'],
            'g': ['9'],
            'l': ['1'],
        }
        
        leet_words = []
        for word in base_words:
            # Create up to 3 leet variations per word to avoid explosion in wordlist size
            for _ in range(3):
                leet_word = list(word)
                num_replacements = min(3, len(word))  # Replace up to 3 characters
                positions = random.sample(range(len(word)), min(num_replacements, len(word)))
                
                for pos in positions:
                    char = word[pos].lower()
                    if char in leet_replacements:
                        leet_char = random.choice(leet_replacements[char])
                        leet_word[pos] = leet_char
                
                leet_words.append(''.join(leet_word))
        
        base_words.extend(leet_words)
        
        # Add common password patterns
        common_patterns = [
            "password", "pass", "123456", "qwerty", "admin", "welcome",
            "letmein", "abc123", "monkey", "1234567890"
        ]
        
        common_variations = []
        for pattern in common_patterns:
            if self.min_password_length <= len(pattern) <= self.max_password_length:
                common_variations.append(pattern)
                
            # Combine with company name or initials
            if "company_short" in self.target_info and self.target_info["company_short"]:
                company_short = self.target_info["company_short"].lower()
                combined = f"{pattern}{company_short}"
                if self.min_password_length <= len(combined) <= self.max_password_length:
                    common_variations.append(combined)
        
        base_words.extend(common_variations)
        
        # Filter by length constraints and add to wordlist
        filtered_words = self.filter_by_length(base_words)
        self.wordlist.update(filtered_words)
        
        # If we don't have enough passwords, generate more with random numbers/special chars
        if len(self.wordlist) < self.password_count:
            self.generate_additional_passwords()
            
        logger.info(f"Generated {len(self.wordlist)} password variations")
    
    def generate_additional_passwords(self) -> None:
        """Generate additional passwords if we don't have enough."""
        logger.info("Generating additional passwords to meet the requested count...")
        
        base_words = list(self.wordlist)
        additional_needed = self.password_count - len(self.wordlist)
        
        if additional_needed <= 0:
            return
            
        # Add random numbers and special characters to existing words
        special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/"
        
        additional_words = []
        while len(additional_words) < additional_needed:
            # Pick a random base word
            if not base_words:
                break  # No base words to work with
                
            base = random.choice(base_words)
            
            # Add 1-3 random digits
            num_digits = random.randint(1, 3)
            digits = ''.join(random.choices(string.digits, k=num_digits))
            
            # Add 0-2 random special characters
            num_special = random.randint(0, 2)
            special = ''.join(random.choices(special_chars, k=num_special))
            
            # Position: beginning, end, or both
            position = random.choice(["begin", "end", "both"])
            
            if position == "begin":
                new_word = f"{digits}{special}{base}"
            elif position == "end":
                new_word = f"{base}{digits}{special}"
            else:  # both
                new_word = f"{digits}{base}{special}"
            
            # Check length constraints
            if self.min_password_length <= len(new_word) <= self.max_password_length:
                additional_words.append(new_word)
        
        self.wordlist.update(additional_words)
        
        # If we still need more passwords, generate completely random ones
        still_needed = self.password_count - len(self.wordlist)
        if still_needed > 0:
            logger.info(f"Generating {still_needed} random passwords to meet the requested count")
            
            chars = string.ascii_letters + string.digits + special_chars
            for _ in range(still_needed):
                # Generate random length between min and max
                length = random.randint(self.min_password_length, self.max_password_length)
                random_pass = ''.join(random.choices(chars, k=length))
                self.wordlist.add(random_pass)
    
    def save_wordlist(self) -> None:
        """Save the generated wordlist to a file."""
        # Convert set to list and limit to requested count
        wordlist = list(self.wordlist)
        random.shuffle(wordlist)  # Shuffle for randomization
        wordlist = wordlist[:self.password_count]  # Limit to requested count
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for password in wordlist:
                f.write(f"{password}\n")
        
        logger.info(f"Wordlist saved to {self.output_file} with {len(wordlist)} passwords")
        print(f"\nWordlist with {len(wordlist)} passwords saved to: {self.output_file}")
    
    def display_banner(self) -> None:
        """Display a fancy banner with title and author info."""
        try:
            banner = pyfiglet.figlet_format("AI-F0RC3", font="slant")
            print("\n" + banner)
            print("=" * 60)
            print("Created by: 7wh0Am-i".center(60))
            print(f"GitHub: https://github.com/7wh0Am-i".center(60))
            print("=" * 60 + "\n")
        except ImportError:
            # If pyfiglet is not available, display a simple banner
            print("\n" + "=" * 60)
            print("AI-F0RC3".center(60))
            print("=" * 60)
            print("Created by: 7wh0Am-i".center(60))
            print(f"GitHub: https://github.com/7wh0Am-i".center(60))
            print("=" * 60 + "\n")
            
    def run(self) -> None:
        """Run the wordlist generation process."""
        # Display banner
        self.display_banner()
        
        # Collect target information
        self.collect_target_info()
        
        # Generate password variations
        self.generate_variations()
        
        # Save the wordlist
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
        
        print("\nDone! Your custom wordlist is ready for use.")
        print("REMINDER: Only use this tool for ethical and authorized testing.")
    
    def prepare_for_hydra(self, target: str, service: str) -> str:
        """
        Prepare a Hydra command for brute-force testing.
        
        Args:
            target: The target IP or hostname
            service: The service to attack (ssh, ftp, http-post-form, smb)
            
        Returns:
            str: The prepared Hydra command
        """
        if not os.path.exists(self.output_file):
            logger.error(f"Wordlist file {self.output_file} not found.")
            return ""
        
        # Construct username list from target info
        username_file = f"usernames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        usernames = []
        
        if "first_name" in self.target_info and self.target_info["first_name"]:
            usernames.append(self.target_info["first_name"].lower())
        
        if "last_name" in self.target_info and self.target_info["last_name"]:
            usernames.append(self.target_info["last_name"].lower())
            
        if "first_name" in self.target_info and "last_name" in self.target_info:
            if self.target_info["first_name"] and self.target_info["last_name"]:
                usernames.append(f"{self.target_info['first_name'].lower()}{self.target_info['last_name'].lower()}")
                usernames.append(f"{self.target_info['first_name'][0].lower()}{self.target_info['last_name'].lower()}")
        
        if "nickname" in self.target_info and self.target_info["nickname"]:
            usernames.append(self.target_info["nickname"].lower())
        
        # Add common usernames if not enough are available
        if len(usernames) < 3:
            common_usernames = ["admin", "administrator", "root", "user", "guest", "test", "support", "sysadmin"]
            usernames.extend(common_usernames)
        
        # Make usernames unique
        usernames = list(set(usernames))
        
        try:
            with open(username_file, 'w', encoding='utf-8') as f:
                for username in usernames:
                    f.write(f"{username}\n")
            logger.info(f"Username list saved to {username_file} with {len(usernames)} usernames")
        except Exception as e:
            logger.error(f"Error saving username file: {str(e)}")
            return ""
        
        # Construct the Hydra command
        hydra_cmd = f"hydra -L {username_file} -P {self.output_file} {target} {service}"
        
        if service == "http-post-form":
            form_path = input("HTTP form path (e.g., /login.php): ").strip()
            form_params = input("Form parameters (e.g., user=^USER^&pass=^PASS^): ").strip()
            failure_string = input("Failure string (text that appears when login fails): ").strip()
            hydra_cmd = f"hydra -L {username_file} -P {self.output_file} {target} {service}:\"{form_path}:{form_params}:{failure_string}\""
        elif service == "smb":
            hydra_cmd = f"hydra -L {username_file} -P {self.output_file} {target} {service}"
        
        hydra_cmd += " -t 4 -V"
        
        logger.info(f"Prepared Hydra command: {hydra_cmd}")
        return hydra_cmd

def main():
    """Main function to run the target wordlist generator."""
    generator = TargetWordlistGenerator()
    generator.run()

if __name__ == "__main__":
    main()
