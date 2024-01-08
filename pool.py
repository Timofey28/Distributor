

class Group:
    def __init__(self, line: str):
        self.line = line
        self.id = int(line[:line.find(' ')])
        line = line[line.find(' ') + 1:]
        self.screen_name = line[:line.find(' ')]
        line = line[line.find(' ') + 1:]
        self.followers_amount = int(line[:line.find(' ')])
        line = line[line.find(' ') + 1:]
        self.type = line[:line.find(' ')]
        self.post_id = int(line[line.find(' ') + 1:])

    def __str__(self):
        return self.line[:-1]

    def __repr__(self):
        return self.line


class Pool:
    def __init__(self, path: str):
        self.path = path
        self.groups = []
        with open(path) as file:
            lines = file.readlines()
        lines = list(filter(lambda x: x != '\n', lines))
        for line in lines:
            self.groups.append(Group(line))

    def __str__(self):
        return self.path[self.path.rfind('/') + 1:-7].replace('_', ' ')

    def __len__(self):
        return len(self.groups)

    def __getitem__(self, item):
        return self.groups[item]

    def write_back(self, path=None):
        if path is None:
            path = self.path
        with open(path, "w", encoding="utf-8") as file:
            for group in self.groups:
                file.write(repr(group))
