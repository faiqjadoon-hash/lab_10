from collections import deque


def eval_rpn(tokens):
    # Outline:
    #   Restate: evaluate a postfix expression; "/" truncates toward zero.
    #   By hand: ["2","1","+","3","*"] -> push 2, push 1, "+" pops 1 and 2, pushes 3;
    #            push 3, "*" pops 3 and 3, pushes 9.
    #   Approach: stack of ints. Number -> push. Operator -> pop b, then a (order matters
    #            for - and /), push a op b. The answer is the last item left on the stack.
    stack = []
    for tok in tokens:
        if tok in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(tok))
    return stack[-1]


def decode_string(s):
    # Outline:
    #   Restate: expand k[encoded], possibly nested.
    #   By hand: "3[a2[c]]" -> at the first "[" save ("", 3); at the second save ("a", 2);
    #            inside is "c"; "]" -> "a" + "c"*2 = "acc"; "]" -> "" + "acc"*3.
    #   Approach: keep cur (text being built) and num (count being read). On "[" push
    #            (cur, num) and reset. On "]" pop (prev, k) and set cur = prev + cur * k.
    #            Digits build num (may be multi-digit); letters append to cur.
    stack = []
    cur = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, num))
            cur = ""
            num = 0
        elif ch == "]":
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur


def daily_temperatures(temps):
    # Outline:
    #   Restate: for each day, count days until a warmer one (0 if none).
    #   By hand: [30,40,50,60] -> each day is resolved by the very next day -> [1,1,1,0].
    #   Approach: stack of indices of days still waiting for a warmer day. For each day i,
    #            while the top day is colder than temps[i], pop it and set
    #            answer[top] = i - top. Then push i. Leftovers stay 0.
    answer = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def num_islands(grid):   # Part 4 - stretch (optional)
    # Outline:
    #   Restate: count groups of "1"s connected up/down/left/right.
    #   By hand: scan cells; at an unvisited "1", flood outward, marking all connected
    #            land; each time that starts, count += 1.
    #   Approach: BFS with a queue and a visited set.
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                count += 1
                visited.add((r, c))
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == "1" and (nr, nc) not in visited):
                            visited.add((nr, nc))
                            queue.append((nr, nc))
    return count


def main():
    print(eval_rpn(["2", "1", "+", "3", "*"]))                 # 9
    print(eval_rpn(["4", "13", "5", "/", "+"]))                # 6
    print(decode_string("3[a2[c]]"))                           # accaccacc
    print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))  # [1,1,4,2,1,1,0,0]
    print(num_islands(["11000", "11000", "00100", "00011"]))   # 3


if __name__ == "__main__":
    main()