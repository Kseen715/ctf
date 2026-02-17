# Catches <div id="auto-sort-start"/> and <div id="auto-sort-end"/> in
# all README.md files in current folder and subfolders. Then sorts the lines 
# between them alphabetically.
#
# 
# 
# The script also creates a hash file for each README.md file to keep track of
# changes. If the hash file is missing or the hash does not match, the script
# will warn the user that the file has been modified.
# 
# v1.2.0


import re, os, datetime, hashlib


# To drop the following imports and whole requirements.txt file:
# ==============================================================================
# Part of colorama.py module
# ==============================================================================
# colorama's LICENSE:
"""
Copyright (c) 2010 Jonathan Hartley
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holders, nor those of its contributors
  may be used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# 
# 
CSI = '\033['
# 
# 
def code_to_chars(code):
    return CSI + str(code) + 'm'
# 
# 
class colorama:
    class AnsiCodes(object):
        def __init__(self):
            # the subclasses declare class attributes which are numbers.
            # Upon instantiation we define instance attributes, which are the 
            # same as the class attributes but wrapped with the ANSI escape 
            # sequence
            for name in dir(self):
                if not name.startswith('_'):
                    value = getattr(self, name)
                    setattr(self, name, code_to_chars(value))
    # 
    # 
    class AnsiFore(AnsiCodes):
        BLACK           = 30
        RED             = 31
        GREEN           = 32
        YELLOW          = 33
        BLUE            = 34
        MAGENTA         = 35
        CYAN            = 36
        WHITE           = 37
        RESET           = 39
    # 
        # These are fairly well supported, but not part of the standard.
        LIGHTBLACK_EX   = 90
        LIGHTRED_EX     = 91
        LIGHTGREEN_EX   = 92
        LIGHTYELLOW_EX  = 93
        LIGHTBLUE_EX    = 94
        LIGHTMAGENTA_EX = 95
        LIGHTCYAN_EX    = 96
        LIGHTWHITE_EX   = 97
    # 
    # 
    class AnsiStyle(AnsiCodes):
        BRIGHT    = 1
        DIM       = 2
        NORMAL    = 22
        RESET_ALL = 0
    # 
    # 
    Fore   = AnsiFore()
    Style  = AnsiStyle()
# ==============================================================================
# End of colorama.py module
# ==============================================================================


class Logger:
    LOG_LEVELS = {
        'NONE': 0,
        'ERROR': 1,
        'WARNING': 2,
        'SUCCESS': 3,
        'INFO': 4,
        'DEBUG': 5,
    }

    LOG_LEVEL = LOG_LEVELS['DEBUG']

    @staticmethod
    def debug(msg):
        """Log debug message

        Args:
            msg (str): Debug message
        """
        if Logger.LOG_LEVEL >= Logger.LOG_LEVELS['DEBUG']:
            print(f'{colorama.Fore.CYAN}{datetime.datetime.now()} ' \
                  + f'[DEBUG] {msg}{colorama.Style.RESET_ALL}')

    @staticmethod
    def info(msg):
        """Log info message

        Args:
            msg (str): Info message
        """
        if Logger.LOG_LEVEL >= Logger.LOG_LEVELS['INFO']:
            print(f'{colorama.Style.RESET_ALL}{datetime.datetime.now()} ' \
                  + f'[INFO] {msg}{colorama.Style.RESET_ALL}')

    @staticmethod
    def happy(msg):
        """Log happy message

        Args:
            msg (str): Happy message
        """
        if Logger.LOG_LEVEL >= Logger.LOG_LEVELS['SUCCESS']:
            print(f'{colorama.Fore.GREEN}{datetime.datetime.now()} ' \
                  + f'[SUCCESS] {msg}{colorama.Style.RESET_ALL}')

    @staticmethod
    def warning(msg):
        """Log warning message

        Args:
            msg (str): Warning message
        """
        if Logger.LOG_LEVEL >= Logger.LOG_LEVELS['WARNING']:
            print(f'{colorama.Fore.YELLOW}{datetime.datetime.now()} ' \
                  + f'[WARNING] {msg}{colorama.Style.RESET_ALL}')

    @staticmethod
    def error(msg):
        """Log error message

        Args:
            msg (str): Error message
        """
        if Logger.LOG_LEVEL >= Logger.LOG_LEVELS['ERROR']:
            print(f'{colorama.Fore.RED}{datetime.datetime.now()} ' \
                  + f'[ERROR] {msg}{colorama.Style.RESET_ALL}')


def read_file_binary(filename):
    """Read binary data from file

    Args:
        filename (str): Name of the file to read data

    Returns:
        bytes: Binary data read from file
    """
    with open(filename, 'rb') as f:
        return f.read()


def hash_file(filename):
    """Hash file

    Args:
        filename (str): Name of the file to hash

    Returns:
        bytes: Hash of the file in bytes
    """
    return hashlib.sha256(read_file_binary(filename)).digest()


def save_hash_binary(new_hash_bytes, new_hash_filename):
    """Save hash of binary data to file

    Args:
        data (bytes): Binary data to hash
        filename (str): Name of the file to save hash
    """
    with open(new_hash_filename, 'wb') as f:
        f.write(new_hash_bytes)
    Logger.info(f'Saved hash to {new_hash_filename}')


def check_hash_binary(new_hash_bytes, old_hash_filename):
    """Check hash of binary data

    Args:
        data (bytes): Binary data to hash
        filename (str): Name of the file to check hash

    Returns:
        bool: Whether the hash matches
    """
    return new_hash_bytes == read_file_binary(old_hash_filename)


def convert_file_name_to_hash_name(file_path: str):
    """Convert file name to hash name

    Args:
        file_path (str): Full path of the file

    Returns:
        str: Full path of the hash file
    """
    # Replace / and \\ with _
    hash_name = file_path.replace('/', '_').replace('\\', '_')
    # Append .hash extension
    hash_name += '.hash'
    #  Join hashes folder
    hash_name = os.path.join('hashes', hash_name)
    return hash_name


def sort_readme(file_path: str):
    Logger.info('sort_readme: Starting')
    hashfile_path = convert_file_name_to_hash_name(file_path)
    if not os.path.exists('hashes'):
        os.makedirs('hashes')
    if os.path.exists(hashfile_path):
        if not check_hash_binary(hash_file(file_path), hashfile_path):
            Logger.warning(f'{file_path} has been modified')
        else:
            Logger.info(f'{file_path} has not been modified')
            Logger.info('sort_readme: Finished')
            return
    else:
        Logger.warning(f'No hash file found for {file_path}. '\
                       + 'New hash will be created')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        readme = f.readlines()
    
    def sort_block(lines):
        """Recursively sort blocks marked with auto-sort-start/end tags"""
        sorted_lines = []
        i = 0
        while i < len(lines):
            if '<div id="auto-sort-start"/>' in lines[i]:
                sorted_lines.append(lines[i])
                i += 1
                start = i
                
                # Find matching end tag with proper nesting support
                depth = 1
                while i < len(lines) and depth > 0:
                    if '<div id="auto-sort-start"/>' in lines[i]:
                        depth += 1
                    elif '<div id="auto-sort-end"/>' in lines[i]:
                        depth -= 1
                        if depth == 0:
                            break
                    i += 1
                
                end = i
                block_content = lines[start:end]
                
                # Find nested blocks at the immediate next level
                nested_blocks = []
                j = 0
                while j < len(block_content):
                    if '<div id="auto-sort-start"/>' in block_content[j]:
                        nested_start = j
                        depth = 1
                        j += 1
                        while j < len(block_content) and depth > 0:
                            if '<div id="auto-sort-start"/>' in block_content[j]:
                                depth += 1
                            elif '<div id="auto-sort-end"/>' in block_content[j]:
                                depth -= 1
                            j += 1
                        nested_end = j
                        nested_blocks.append((nested_start, nested_end))
                    else:
                        j += 1
                
                if nested_blocks:
                    # Extract blocks to sort (text + nested blocks as units)
                    blocks_to_sort = []
                    prev_end = 0
                    for nested_start, nested_end in nested_blocks:
                        # Add text before nested block (skip if empty/whitespace only)
                        if nested_start > prev_end:
                            text_block = block_content[prev_end:nested_start]
                            if any(line.strip() for line in text_block):
                                blocks_to_sort.append(text_block)
                        # Add nested block (recursively sort its content)
                        nested_block = block_content[nested_start:nested_end]
                        sorted_nested = sort_block(nested_block)
                        blocks_to_sort.append(sorted_nested)
                        prev_end = nested_end
                    # Add remaining text after last nested block (skip if empty/whitespace only)
                    if prev_end < len(block_content):
                        text_block = block_content[prev_end:]
                        if any(line.strip() for line in text_block):
                            blocks_to_sort.append(text_block)
                    
                    # Sort blocks by their text content (strip markdown for comparison)
                    sorted_blocks = sorted(blocks_to_sort, 
                                         key=lambda block: ''.join(block).lower().strip())
                    for block in sorted_blocks:
                        sorted_lines.extend(block)
                else:
                    # No nested blocks - just sort lines (filter empty lines)
                    non_empty_lines = [line for line in block_content if line.strip()]
                    sorted_lines.extend(sorted(non_empty_lines, key=lambda line: line.lower().strip()))
                
                # Add the closing tag
                if i < len(lines):
                    sorted_lines.append(lines[i])
                    i += 1
            else:
                sorted_lines.append(lines[i])
                i += 1
        
        return sorted_lines
    
    sorted_readme = sort_block(readme)
    
    def format_markdown(lines):
        """Add proper spacing to markdown following standard formatting rules"""
        formatted = []
        i = 0
        while i < len(lines):
            line = lines[i]
            prev_line = lines[i-1] if i > 0 else ''
            next_line = lines[i+1] if i < len(lines) - 1 else ''
            
            # Before ## headers, add blank line if previous isn't blank/start tag
            if line.strip().startswith('- ##'):
                if prev_line.strip() and '<div id="auto-sort-start"/>' not in prev_line:
                    formatted.append('\n')
            
            # Add current line
            formatted.append(line)
            
            # Determine if we need a blank line after current line
            need_blank = False
            
            # After auto-sort-start tag, add blank line if next is content (MD033)
            if '<div id="auto-sort-start"/>' in line:
                if next_line.strip() and next_line.strip().startswith('- ##'):
                    need_blank = True
            
            # After headers (##), add blank line if next isn't blank/tag/another header
            if line.strip().startswith('#') and not line.strip().startswith('####'):
                if next_line.strip() and not next_line.strip().startswith('#') and \
                   '<div id="auto-sort' not in next_line:
                    need_blank = True
            
            # Between different list levels (- ## and  - `)
            if line.strip().startswith('- ##') and next_line.strip().startswith('  -'):
                need_blank = True
            
            # After end of nested block, before next item at same level
            if '<div id="auto-sort-end"/>' in line:
                if next_line.strip() and not '<div id="auto-sort-end"/>' in next_line and \
                   not next_line.strip().startswith('<div id="auto-sort-start"/>') and \
                   not next_line.strip().startswith('- ##'):
                    need_blank = True
            
            # Add blank line if needed and next line isn't already blank
            if need_blank and next_line.strip():
                formatted.append('\n')
            
            i += 1
        
        return formatted
    
    formatted_readme = format_markdown(sorted_readme)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(formatted_readme)
    
    Logger.happy(f'Sorted {file_path}')
    save_hash_binary(hash_file(file_path), hashfile_path)
    Logger.info('sort_readme: Finished')

def search_readmes():
    Logger.info('search_readmes: Starting')
    res = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'README.md':
                res.append(os.path.join(root, file))
                Logger.info(f'Found README.md at {os.path.join(root, file)}')
    Logger.info('search_readmes: Finished')
    return res


if __name__ == '__main__':
    [sort_readme(readme) for readme in search_readmes()]
