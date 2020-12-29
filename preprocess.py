import re

class Preprocessor():
    def __init__(self, src=None, dest=None):
        self.src = src
        self.dest = dest
        # re.compile(r'(?<!!)\[(.+)?\]\((.+)?\)')
        # rather than using a negative lookahead assertion, we use the
        # assumption that subpages exist on their own lines
        self.page_links = re.compile(r'^\[(.+)?\]\((.+)?\)$')
        self.hyperlinks = re.compile(r'https://.*?\.com')
        
    
    # take all of the subpages within an md file and combine them all
    # into a single md file
    # this creates a new md file rather than overwriting the original
    # file
    def aggregate(self):
        with open(self.dest, 'w') as dest_stream:

            src_dir = '/'.join(self.src.split('/')[:-1])

            with open(self.src, 'r') as page:
                self.__read_page(page, src_dir, dest_stream)

            # remember to close the src i/o objects
            dest_stream.flush()
    
    def __read_page(self, page_itr, page_path, dest_stream):
        for line in page_itr:
            # notion only allows for one subpage link per line
            # so we only need to check for one match per line
            subpage = self.page_links.search(line)

            if subpage:
                non_page = self.hyperlinks.search(line)

                if non_page:
                    dest_stream.write(line)
                    continue

                subpage_name, subpage_loc = subpage.groups()
                subpage_loc = subpage_loc.replace('%20', ' ').split('/')
                print(subpage_name)

                # notion exports are structured so that
                # subpages are a direct child directory of the
                # directory that parent page is in
                subpage_path = page_path + '/' + subpage_loc[0]
                print(subpage_path)

                subpage_loc = subpage_path + '/' + subpage_loc[1]

                try:
                    with open(subpage_loc, 'r') as subpage:
                        self.__read_page(subpage, subpage_path, dest_stream)
                except FileNotFoundError:
                    # notion handles links to subpages and actual hyperlinks in the same way
                    # if the file is not found, there may be an issue or it may actually be
                    # a hyperlink
                    print('error opening the subpage')
            else:
                dest_stream.write(line)


    # set the new src and dest md files
    def set_target(self, new_src, new_dest):
        self.src = new_src
        self.dest = new_dest
        return

if __name__ == "__main__":
    output = 'test_case/intermediate.md'
    input_file = "test_case/Personal Projects ec668bf9a7814cc7bf4be870bcd8d7fe/Not yet started 6c519e7e7356463284ab8b8e16e2b33d/dp3t app implementation efb79115e1f94a95bd2b4af0d1b216c2.md"
    #"test_case/Personal Projects ec668bf9a7814cc7bf4be870bcd8d7fe.md"
    #"../notion2pdf/test_case/COMP 455 705b97e1ae6c4fae84d220e802bc008d.md"

    p = Preprocessor(input_file, output)

    p.aggregate()