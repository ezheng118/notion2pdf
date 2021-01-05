from collections import deque
from datetime import date
import re

class Translator():
    # takes a preprocessed md file and turns it into a tex file
    def __init__(self, input_path=None, output_path=None, doc_author=None):
        self.input = input_path
        self.output = output_path
        self.author = doc_author

        self.env_stack = deque()
        #self.sections = []
    
    def convert_md2latex(self):
        output_file = open(self.output, 'w')
        input_file = open(self.input, 'r')

        # rules
        # section headers placed on their own lines (indicated by #'s)
        # dividers are placed on their own lines (---)
        # latex encapsulated by $$~$$ or $~$ is already correct and can be ignored
        # (- ) indicates some kind of nested bullet point structure
        # numbered lists also appear
        # links are specified by [~](~)
        # links to images are specified by ![~](~)
        # **~** bolds
        # *~* italicizes

        header_pattern = re.compile(r'^(#{1,3}) (.*)\n$')
        bullet_pt_pattern = re.compile(r'^(\t*)- (.*)\n')

        self.setup_doc(output_file)

        num_indents = 0

        for line in input_file:
            latex_line = ''
            
            if line[0] == '\n':
                if self.env_stack[-1]:
                    latex_line += "\\end{" + self.env_stack[-1] + "}\n"

                latex_line += '\n'
            elif line[0] == '#':
                mo = header_pattern.search(line)

                if mo:
                    latex_line += '\\'
                    if len(mo.group(1)) == 2:
                        latex_line += 'sub'
                    elif len(mo.group(1)) == 3:
                        latex_line += 'subsub'
                    latex_line += 'section*{' + mo.group(2) + '}\n'
                else:
                    latex_line = self.parse_line(line)
            elif line[0] == '-':
                if line[1:4] == '--\n':
                    latex_line += "\\begin{center}\n\t\\rule{320pt}{.5pt}\n"
                    self.env_stack.append('center')
                else:
                    latex_line = "\\begin{itemize}\n\t\\item " + line[3:] + "\n"
            elif line[0] == '\t':
                # Todo: handle indenting
                print('do something')
            else:
                latex_line = self.parse_line(line)
            print(latex_line)

            output_file.write(latex_line)

        output_file.close()
        input_file.close()
    
    def setup_doc(self, out_stream):
        setup_str = "\\documentclass{article}\n"\
                    "\\usepackage[utf8]{inputenc}\n\n"
        
        metadata = "\\title{}\n"\
                    "\\author{" + self.author + "}\n"\
                    "\\date{" + date.today().strftime("%B %d, %Y")+ "}\n\n"
        
        b = "\\begin{document}\n"
        
        out_stream.write(setup_str)

        out_stream.write(metadata)

        # begin document env dealt with seperately instead of using the stack
        out_stream.write(b)
    
    def parse_line(self, line):
        return print(line)

if __name__ == "__main__":
    print('translator')

    inp = "test_case/intermediate.md"
    output = "test_case/output.tex"

    t = Translator(inp, output, "erzh")

    t.convert_md2latex()