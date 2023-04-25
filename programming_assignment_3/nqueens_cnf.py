def generate_cnf_file(N, filename):
    def write_clauses(f, clauses):
        for clause in clauses:
            f.write(' '.join(clause) + '\n')

    with open(filename, 'w') as f:
        # At least one queen in each row
        for r in range(1, N + 1):
            row_clause = [f"Q{c}{r}" for c in range(1, N + 1)]
            f.write(' '.join(row_clause) + '\n')

        # At least one queen in each column
        for c in range(1, N + 1):
            col_clause = [f"Q{c}{r}" for r in range(1, N + 1)]
            f.write(' '.join(col_clause) + '\n')

        # No two queens in the same row or column
        for q1 in range(1, N + 1):
            for q2 in range(1, N + 1):
                if q1 != q2:
                    for i in range(1, N + 1):
                        f.write(f"-Q{q1}{i} -Q{q2}{i}\n")
                        f.write(f"-Q{i}{q1} -Q{i}{q2}\n")

        # No two queens on the same diagonal
        for c1 in range(1, N + 1):
            for r1 in range(1, N + 1):
                for c2 in range(1, N + 1):
                    for r2 in range(1, N + 1):
                        if c1 != c2 and r1 != r2 and abs(c1 - c2) == abs(r1 - r2):
                            f.write(f"-Q{c1}{r1} -Q{c2}{r2}\n")

for N in range(3, 7):
    generate_cnf_file(N, f"{N}queens.cnf")