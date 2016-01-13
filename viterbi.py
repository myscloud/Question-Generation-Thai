
def viterbi(self, obs, states, initp, trans, emiss):
        obs_count = len(obs)
        vtb = [{}] * (obs_count)
        path = {}

        # initialize base case
        for state in states:
            vtb[0][state] = initp.at(state) * emiss.at(obs[0])[state]
            path[state] = [state]

        # run viterbi for t > 0
        for t in range(1, 6):
            new_path = {}
            for state in states:
                (prob, max_prev_state) = max(((vtb[t-1][prev_state] * trans.at(prev_state)[state] * emiss.at(obs[t])[state]), prev_state) for prev_state in states)
                vtb[t][state] = prob
                new_path[state] = path[max_prev_state] + [state]

            path = new_path
            (_, state) = max((vtb[t][st], st) for st in states)
            print(str(t) + " " + obs[t] + " " + state)
            print(str(emiss.at(obs[t])))

        # (prob, state) = max((vtb[obs_count-1][st], st) for st in states)
        (prob, state) = max((vtb[5][st], st) for st in states)
        print(state)
        return path[state]