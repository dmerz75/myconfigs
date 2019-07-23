import itertools

class VolleyballTournament:
    """ The plotting class for SOP,GSOP,and SOPNucleo trajectories.
    """
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    def print_list(self, obj):

        for o in obj:
            print(o)


    def construct_team_pairings(self, team, teamname="team1"):

        team_name_final = teamname + "_pairs"
        mates = list(itertools.combinations(team, 2))
        setattr(self, team_name_final, mates)

    def construct_matches(self, lst_teams):
        """
        :param lst_teams: at least 2 teams, maybe only 2.
        :return:
        """
        self.matches = list(itertools.product(*lst_teams))

