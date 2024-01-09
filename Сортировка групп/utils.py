import os

pool_path = "../path/to/the/pool.txt"


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


class Screenshots:
    def __init__(self, pool: Pool):
        self.pool = pool
        if not os.path.exists("screenshots"):
            print("No screenshots folder found. Please, run gather_screenshots.py first.")
            exit(0)
        self.clubs = []
        self.decisions = []
        if os.path.exists("screenshots/progress.txt"):
            with open("screenshots/progress.txt") as file:
                lines = file.readlines()
            self.clubs = list(map(lambda x: x[:x.find(' ')], lines))
            self.decisions = list(map(lambda x: x[x.find(' ') + 1:-1], lines))
        else:
            self.clubs = [x.screen_name for x in pool.groups]
            self.decisions = ['unclear' for _ in range(len(pool))]

    def __len__(self):
        return len(self.clubs)

    def calculate_progress(self):
        return len(list(filter(lambda x: x != 'unclear', self.decisions)))

    def get_next_unclear_club(self, current_club_no=0):
        if current_club_no >= len(self.clubs) or current_club_no == 0:
            for i in range(len(self.clubs)):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
        else:
            for i in range(current_club_no, len(self.clubs)):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
            for i in range(current_club_no):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
        return None

    def get_previous_unclear_club(self, current_club_no=0):
        if current_club_no >= len(self.clubs) or current_club_no == 0:
            for i in range(len(self.clubs) - 1, -1, -1):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
        else:
            for i in range(current_club_no - 1, -1, -1):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
            for i in range(len(self.clubs) - 1, current_club_no - 1, -1):
                if self.decisions[i] == 'unclear':
                    return self.clubs[i]
        return None

    def write_decision(self, decision: str, club_no: int):
        assert(decision in ['positive', 'negative', 'unclear'])
        assert(1 <= club_no <= len(self.clubs))
        self.decisions[club_no - 1] = decision

    def save(self):
        with open("screenshots/progress.txt", "w") as file:
            for i in range(len(self.clubs)):
                file.write(f"{self.clubs[i]} {self.decisions[i]}\n")

    def make_pool_file(self):
        assert(len(list(filter(lambda x: x == 'unclear', self.decisions))) == 0)
        positive_clubs = list(filter(lambda x: x[1] == 'positive', zip(self.clubs, self.decisions)))
        positive_clubs = set(x[0] for x in positive_clubs)
        with open(pool_path[pool_path.rfind('/') + 1:], "w") as file:
            for i in range(len(self.clubs)):
                if self.clubs[i] in positive_clubs:
                    file.write(self.pool[i].line)
