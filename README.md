# AI-F0rc3

A Python-based toolkit for generating custom wordlists for authorized password testing, featuring both personal and target-focused approaches.

## ⚠️ Ethical Use Disclaimer

This toolkit is designed **ONLY** for:
- Ethical security testing
- Systems you own
- Systems you have explicit written permission to test

**Unauthorized password attacks are illegal and can result in serious legal consequences.**

## Available Tools

### 1. wordlist_generator.py
Generate wordlists based on personal information with optional AI integration.

### 2. target_wordlist_generator.py
Create customized wordlists specifically focused on a target entity, with options to specify password count and length.

## Features

- Two complementary approaches to wordlist generation
- Customizable password count and length requirements
- Generate target-specific or personal wordlists
- Creates common password variations and combinations
- Integrates with multiple AI APIs for creative password variations:
  - OpenAI (GPT-3.5 Turbo)
  - Google Gemini Pro
  - Grok
  - DeepSeek R1
  - Llama 3
- Supports password length constraints (minimum and maximum)
- Prepares commands for Hydra brute-force testing
- Comprehensive logging for all operations
- Detailed help system for all functions and options

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - requests
  - pyfiglet
- hydra (optional for brute-force testing)
```bash
sudo apt install hydra
```

## Installation

1. Clone this repository or download the source code
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Personal Wordlist Generator

#### Basic Usage

Run the script without arguments for interactive mode:

```bash
python wordlist_generator.py
```

### Command-line Arguments

```bash
python wordlist_generator.py [options]
```

Options:
- `--use-ai`: Enable AI-powered password variations (requires API key)
- `--api-key KEY`: Specify the API key for AI integration
- `--api-provider {openai,gemini,grok,deepseek,llama3}`: Choose which AI provider to use (default: openai)
- `--api-base-url URL`: Optional custom API base URL for self-hosted models or alternative endpoints
- `--min-length NUM`: Specify minimum password length
- `--max-length NUM`: Specify maximum password length
- `--output FILE`: Specify a custom output filename for the wordlist
- `--help-function NAME`: Display detailed help for a specific function
- `--show-functions`: List all available functions
- `--help-options`: Display detailed help for all command-line options

### Examples

Using OpenAI with password length constraints:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_OPENAI_API_KEY --min-length 8 --max-length 16 --output my_wordlist.txt
```

Getting detailed help on command options:
```bash
python wordlist_generator.py --help-options
```

Viewing help for a specific function:
```bash
python wordlist_generator.py --help-function generate_ai_variations
```

Listing all available functions:
```bash
python wordlist_generator.py --show-functions
```

Using Google Gemini:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_GEMINI_API_KEY --api-provider gemini --output my_wordlist.txt
```

### Target Wordlist Generator

The target-based generator focuses on creating wordlists based on information about a specific target entity.

#### Basic Usage

Run the script for interactive mode:

```bash
python target_wordlist_generator.py
```

#### Features

- Specify exactly how many passwords you need in the wordlist
- Set minimum and maximum password lengths
- Collect specific information about your target
- Optional organization/company information
- Optional personal details (pet names, spouse, etc.)
- Optional important dates
- Creates a customized output file with timestamp
- Prepares Hydra commands for testing
```

Using Grok:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_GROK_API_KEY --api-provider grok --output my_wordlist.txt
```

Using DeepSeek:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_DEEPSEEK_API_KEY --api-provider deepseek --output my_wordlist.txt
```

Using Llama 3:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_LLAMA3_API_KEY --api-provider llama3 --output my_wordlist.txt
```

Using a custom API endpoint:
```bash
python wordlist_generator.py --use-ai --api-key YOUR_API_KEY --api-provider llama3 --api-base-url http://your-selfhosted-api.com --output my_wordlist.txt
```

## How It Works

1. **Information Collection**: The tool prompts for personal information such as names, pet names, important dates, etc. You can also specify minimum and maximum password lengths.
2. **Basic Variation Generation**: Creates variations using common patterns, capitalizations, number combinations, etc.
3. **Length Filtering**: Filters out passwords that don't meet the specified length constraints.
4. **AI-Powered Generation** (Optional): Uses AI to generate more sophisticated password variations that adhere to the length requirements.
5. **Wordlist Creation**: Saves all unique password variations to a file.
6. **Hydra Integration**: Helps prepare a command for use with Hydra for brute-force testing.

## Built-in Help System

The tool includes a comprehensive help system that provides detailed information about:

- General usage and command-line options
- Complete list of available functions
- Detailed explanations of each function including:
  - Purpose and functionality
  - Required parameters
  - Return values
  - Usage examples

To access the help system:

1. **Standard help**: `python wordlist_generator.py --help` (basic argparse help)
2. **Detailed options help**: `python wordlist_generator.py --help-options` (comprehensive options guide)
3. **List all functions**: `python wordlist_generator.py --show-functions`
4. **Function-specific help**: `python wordlist_generator.py --help-function FUNCTION_NAME`

The `--help-options` command provides detailed information about:
- All available command-line options grouped by category
- Default values and requirements
- Usage examples for common scenarios
- Important notes about the tool's operation

Example functions include:
- `collect_personal_info`
- `generate_basic_variations`
- `generate_ai_variations`
- `filter_by_length`
- `save_wordlist`
- `prepare_for_hydra`
- `run`

## AI Integration

The tool supports multiple AI providers:

### OpenAI
- Uses the GPT-3.5 Turbo model
- Requires an OpenAI API key (https://platform.openai.com/)
- Generally provides high-quality creative variations

### Google Gemini
- Uses the Gemini Pro model
- Requires a Google AI Studio API key (https://makersuite.google.com/)
- May offer different creative perspectives on password combinations

### Grok
- Uses the Grok-1 model from xAI
- Requires a Grok API key
- Known for generating unique variations with different patterns

### DeepSeek
- Uses the DeepSeek R1 model
- Requires a DeepSeek API key
- Specialized in high-performance generation capabilities

### Llama 3
- Uses Meta's Llama 3 model
- Requires an appropriate API key for access
- Open source model with strong general capabilities

### Self-Hosted Models
- You can use your own self-hosted models with the `--api-base-url` parameter
- Works with any API that follows the OpenAI chat completions API format

## Password Length Constraints

You can specify password length constraints in two ways:
1. **Command-line arguments**: Use `--min-length` and `--max-length` options
2. **Interactive input**: When running the tool, you'll be prompted to enter minimum and maximum lengths

Benefits of using length constraints:
- Generate more targeted and realistic password lists
- Reduce wordlist size by filtering out passwords that are too short or long
- Match the target system's password policy (if known)
- Optimize brute-force testing efficiency

## Hydra Integration

The tool can generate Hydra commands for testing against:
- SSH
- FTP
- HTTP Post Form
- SMB

## Performance

The tool uses efficient data structures like Sets to avoid duplicates and ensure optimal performance.

## Logging

All operations are logged to:
- Console output
- `wordlist_generator.log` file

## Choosing the Right Tool

| Feature | wordlist_generator.py | target_wordlist_generator.py |
|---------|----------------------|----------------------------|
| Focus | Personal information | Target entity information |
| AI Integration | Yes | No |
| Password Count | Variable | User-specified exact count |
| CLI Arguments | Extensive | None (fully interactive) |
| Detailed Help | Yes | No |
| Password Length | Optional constraints | Required constraints |
| Output | All generated combinations | Limited to requested count |

Choose **wordlist_generator.py** when:
- You want to generate passwords based on information about yourself
- You need AI-assisted creative variations
- You prefer command-line options
- You need extensive help documentation

Choose **target_wordlist_generator.py** when:
- You're creating a wordlist for testing a specific target
- You need a specific number of passwords
- You want to include company/organization information
- You prefer a guided interactive process

## Advanced Usage Tips

1. **Optimizing Wordlist Size**:
   - Use length constraints to keep wordlists manageable
   - For target_wordlist_generator, specify only the number of passwords you need

2. **Effective Target Profiling**:
   - Collect as much relevant information as possible
   - Include variations of company names and abbreviations
   - Consider interests and hobbies that might influence password choices

3. **Hydra Testing Best Practices**:
   - Use the `-t 4` flag (already included) to limit concurrent attempts
   - Monitor logs carefully to avoid account lockouts
   - Always have explicit permission before testing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the MIT license.

<h2>⚡️ Where to find me</h2>
<p><a target="_blank" href="https://twitter.com/@AnimeshPanna" style="display: inline-block;"><img src="https://img.shields.io/badge/twitter-x?style=for-the-badge&logo=x&logoColor=white&color=%230f1419" alt="twitter" /></a>
<a target="_blank" href="https://dev.to/@soon" style="display: inline-block;"><img src="https://img.shields.io/badge/dev-to?style=for-the-badge&logo=dev-to&logoColor=white&color=black" alt="dev.to" /></a>
<a target="_blank" href="https://www.linkedin.com/in/@non" style="display: inline-block;"><img src="https://img.shields.io/badge/linkedin-logo?style=for-the-badge&logo=linkedin&logoColor=white&color=%230a77b6" alt="linkedin" /></a>
<a target="_blank" href="https://www.instagram.com/@7_who.am__i" style="display: inline-block;"><img src="https://img.shields.io/badge/instagram-logo?style=for-the-badge&logo=instagram&logoColor=white&color=%23F35369" alt="instagram" /></a>
<a target="_blank" href="undefined@soon" style="display: inline-block;"><img src="https://img.shields.io/badge/medium-logo?style=for-the-badge&logo=medium&logoColor=white&color=black" alt="medium" /></a>
<a target="_blank" href="https://stackoverflow.com/users/@soon" style="display: inline-block;"><img src="https://img.shields.io/badge/stackoverflow-logo?style=for-the-badge&logo=stackoverflow&logoColor=white&color=%23cc0000" alt="stackoverflow" /></a></p>

---

Remember: Security testing without explicit authorization is illegal and unethical.
