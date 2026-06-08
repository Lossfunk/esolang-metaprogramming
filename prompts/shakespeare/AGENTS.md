> **Start solving now.** The session is initialized. Begin by fetching your first problem:
> ```
> python harness.py fetch
> ```
> Work through all 80 problems sequentially. For each problem: read the description, generate your own test cases, use `run` to test, then `submit` when confident. Do NOT skip without attempting — see skip policy below.

# EsoLang-Bench: Shakespeare

You are solving 80 shakespeare programming problems sequentially.
Problems span 4 difficulty tiers: E01-E20 (easy), M01-M20 (medium), H01-H20 (hard), X01-X20 (extra-hard).

Each problem has 6 hidden test cases you cannot see. No test cases are provided -- generate your own test inputs from the problem descriptions.

## Harness Commands

```bash
python harness.py fetch                          # Get next problem
python harness.py run <code_file> --input "..."  # Test with custom input (unlimited)
python harness.py submit <problem_id> <file>     # Hidden evaluation (max 3 per problem)
python harness.py status                         # Progress dashboard
python harness.py skip                           # Skip ONLY after attempting (see policy)
```

## Rules

- Solve problems in order. `fetch` advances to the next.
- Maximum 3 submissions per problem. Use `run` (unlimited) to test first.
- `submit` returns PASS/WRONG ANSWER/RUNTIME ERROR per hidden test -- no inputs or expected outputs shown.
- Problem is solved only if 6/6 hidden tests pass.
- Do not read private test files, reverse-engineer the harness, or hardcode outputs.

## CRITICAL: No Skipping — Use All 3 Submissions

- You MUST work on every problem until you either score 6/6 OR use all 3 submissions. Do NOT move to the next problem with unused submissions remaining.
- You CANNOT revisit problems later — once you move on, the problem is gone forever. Every unused submission is wasted.
- There is NO time limit. You have UNLIMITED time and UNLIMITED test runs (`run` command). The ONLY limit is 3 submissions per problem.
- For each problem: read the description, write a genuine solution, test it thoroughly with `run` using multiple inputs until it produces correct output, THEN submit.
- Do NOT submit untested code. Do NOT submit placeholder or stub solutions. Every submission must be a genuine, tested attempt.
- If a submission returns WRONG ANSWER or RUNTIME ERROR: analyze the failure, try a completely different approach, test it, then use your next submission.
- Even if a problem seems extremely difficult, you must use all 3 submissions with genuinely different approaches before moving on. A partial score (1-5/6) is far better than 0/6.
- Do NOT call `fetch` or `skip` to move to the next problem while you still have submissions remaining on the current one.


## Scoring

- Per problem: tests passed / 6
- Overall: problems solved / 80 and total tests passed / 480

## Shakespeare Language Reference

### Program Structure

```
Title.
Character, description.
Act I: Description.
Scene I: Description.
[Enter Character1 and Character2]
Character1:
Statement.
```

### Value System

- **Positive nouns** (+1): angel, cat, day, flower, hero, joy, king, rose, summer, sun
- **Negative nouns** (-1): bastard, beast, coward, death, devil, famine, hell, pig, plague
- **Zero**: `nothing`, `zero`
- **Each adjective doubles**: `a big cat`=2, `a big big cat`=4, `a big big big cat`=8
- **Arithmetic**: `the sum of X and Y`, `the difference between X and Y`, `the product of X and Y`, `the quotient between X and Y`, `the remainder of the quotient between X and Y`, `the square of X`, `twice X`
- **Pronouns**: `you`/`thou`/`thee` = listener's value; `I`/`me` = speaker's value

### Statements (all target the LISTENER)

- **Assign**: `You are EXPR.` / `Thou art EXPR.`
- **Output char**: `Speak your mind.` (listener's value as character)
- **Output number**: `Open your heart.` (listener's value as decimal)
- **Read char**: `Open your mind.` (reads char into listener; -1 at EOF)
- **Read int**: `Listen to your heart.` (reads integer into listener)
- **Stack push**: `Remember EXPR.` (onto listener's stack)
- **Stack pop**: `Recall.` (pop listener's stack into listener's value)

### Comparisons and Flow Control

- `Am I better than EXPR?` (speaker > EXPR)
- `Am I worse than EXPR?` (speaker < EXPR)
- `Am I as good as EXPR?` (speaker == EXPR)
- `If so, let us proceed to Scene X.` (jump if true)
- `If not, let us proceed to Scene X.` (jump if false)
- `Let us proceed to Scene X.` (unconditional jump)

### Stage Rules

- Exactly 2 characters on stage for dialogue.
- `[Enter X and Y]`, `[Exit X]`, `[Exeunt]` (remove all)
- Scene labels use Roman numerals and must be globally unique.

### Common Pitfalls

- **I/O targets the LISTENER**, not the speaker. This is the #1 bug source.
- **No direct numbers**: `You are 72.` is INVALID. Use adjective-noun expressions.
- **Stage management**: Must have exactly 2 characters on stage.
- **Roman numeral scenes must be globally unique** across all Acts.
