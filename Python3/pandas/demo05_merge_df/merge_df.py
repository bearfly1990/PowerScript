import pandas as pd


def merge_csv(csv1_path, csv2_path):
    df_left = pd.read_csv(csv1_path)
    df_right = pd.read_csv(csv2_path)

    # df_merged = pd.merge(df_left, df_right)
    # df_merged = pd.merge(df_left, df_right, on=['SID'])
    # df_merged = pd.merge(df_left, df_right, how='left', on=['SID'])
    # df_merged = pd.merge(df_left, df_right, how='right', on=['SID'])
    df_merged = pd.merge(df_left, df_right, how='outer', on=['SID'])
    print(df_merged)


def concat_csv(csv1_path, csv2_path):
    df_part1 = pd.read_csv(csv1_path)
    df_part2 = pd.read_csv(csv2_path)
    df_concated = pd.concat([df_part1, df_part2])
    df_concated = pd.concat([df_part1, df_part2], ignore_index=True)
    print(df_concated)


def append_csv(csv1_path, csv2_path):
    df_part1 = pd.read_csv(csv1_path)
    df_part2 = pd.read_csv(csv2_path)
    df_append = df_part1.append(df_part2, ignore_index=True)
    print(df_append)


def concat_student_score(file_student, file_score, file_score2):
    df_stu = pd.read_csv(file_student)
    df_score1 = pd.read_csv(file_score)
    df_score2 = pd.read_csv(file_score2)
    df_score = pd.concat([df_score1, df_score2], ignore_index=True)
    # df_score = df_score1.append(df_score2, ignore_index=True)
    df_merged = pd.merge(df_score, df_stu, how='outer', on=['SID'])
    print(df_merged)


if __name__ == '__main__':
    concat_student_score('student.csv', 'score.csv', 'score2.csv')
    # merge_csv('score.csv', 'student.csv')
    # concat_csv('score.csv', 'score2.csv')
    # append_csv('score.csv', 'score2.csv')
