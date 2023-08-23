class Teams:
    def get_team(self, team_name):
        return list(self._gus().soql_query_teams(f"WHERE Name LIKE '%{team_name}%'"))
