# AI-F0rc3

A Python-based tool that generates custom wordlists for password brute-force testing in authorized penetration testing scenarios.

## ⚠️ Ethical Use Disclaimer

This tool is designed **ONLY** for:
- Ethical security testing
- Systems you own
- Systems you have explicit written permission to test

**Unauthorized password attacks are illegal and can result in serious legal consequences.**

## Features

- Generates custom wordlists based on personal information
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

## Installation

1. Clone this repository or download the source code
2. Install the required packages:

```bash
pip install requests
```

## Usage

### Basic Usage

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

## License

Copyright (c) 2025 ANIMESH PANNA 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contribution

Contributions that improve the tool's functionality, performance, or security practices are welcome.

---

Remember: Security testing without explicit authorization is illegal and unethical. 
