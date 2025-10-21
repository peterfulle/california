#!/usr/bin/env python3

def validate_django_template_blocks(filename):
    """Validates that Django template blocks are properly paired"""
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    stack = []
    errors = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Find Django template blocks
        if '{% if ' in line:
            stack.append(('if', i, line))
        elif '{% elif ' in line:
            if not stack or stack[-1][0] not in ['if', 'elif']:
                errors.append(f"Line {i}: 'elif' without matching 'if': {line}")
            else:
                # Replace the last if/elif with elif
                stack[-1] = ('elif', i, line)
        elif '{% else %}' in line:
            if not stack or stack[-1][0] not in ['if', 'elif']:
                errors.append(f"Line {i}: 'else' without matching 'if': {line}")
            else:
                stack[-1] = ('else', i, line)
        elif '{% endif %}' in line:
            if not stack or stack[-1][0] not in ['if', 'elif', 'else']:
                errors.append(f"Line {i}: 'endif' without matching 'if': {line}")
            else:
                stack.pop()
    
    # Check for unmatched blocks
    for block_type, line_num, content in stack:
        errors.append(f"Line {line_num}: Unmatched '{block_type}': {content}")
    
    if errors:
        print("Django Template Block Errors Found:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("All Django template blocks are properly paired!")
        return True

if __name__ == "__main__":
    validate_django_template_blocks("core/templates/core/startup_profile.html")
