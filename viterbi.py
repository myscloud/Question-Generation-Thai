
import math

def viterbi(obs, states, initp, trans, emiss):
        obs_count = len(obs)
        vtb = [{}]
        path = {}
        inf = 10e+20

        # initialize base case
        for state in states:
            vtb[0][state] = initp[state] * emiss[obs[0]][state]
            path[state] = [state]

        # run viterbi for t > 0
        test = obs_count
        for t in range(1, test):
            new_path = {}
            vtb.append({})
            for state in states:
                (prob, max_prev_state) = max(((vtb[t-1][prev_state] * trans[prev_state][state] * emiss[obs[t]][state]), prev_state) for prev_state in states)
                vtb[t][state] = prob
                new_path[state] = path[max_prev_state] + [state]

            path = new_path
            (max_prob, state) = max((vtb[t][st], st) for st in states)
            if max_prob < 10e-15:
                for state in states:
                    vtb[t][state] *= 10e+10
            # print(str(t) + " " + obs[t] + " " + state + " " + str(vtb[t][state]))

        # (prob, state) = max((vtb[obs_count-1][st], st) for st in states)
        (prob, state) = max((vtb[test-1][st], st) for st in states)
        return path[state]