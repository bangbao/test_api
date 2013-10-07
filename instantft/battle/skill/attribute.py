# coding: utf-8

def add_range(rage):
    def wrapper(be, agent, target):
        """
        """

        for agent_id in be.groups[agent.gid]:
            obj = be.agents[agent_id]
            
            if not be.has_agent_dead(agent_id):
                obj.anger += rage

    return wrapper
