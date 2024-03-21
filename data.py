def get_data(conversations: str, movie_lines: str, max_len: int=64) -> list: 

    with open(conversations, 'r', encoding='iso-8859-1') as c:
        conv = c.readlines()
    with open(movie_lines, 'r', encoding='iso-8859-1') as l:
        lines = l.readlines()

    ### splitting text using special lines
    lines_dic = {}
    for line in lines:
        objects = line.split(" +++$+++ ")
        lines_dic[objects[0]] = objects[-1]

    ### generate question answer pairs
    pairs = []
    for con in conv:
        ids = eval(con.split(" +++$+++ ")[-1])
        for i in range(len(ids)):
            qa_pairs = []
            
            if i == len(ids) - 1:
                break

            first = lines_dic[ids[i]].strip()  
            second = lines_dic[ids[i+1]].strip() 

            qa_pairs.append(' '.join(first.split()[:max_len]))
            qa_pairs.append(' '.join(second.split()[:max_len]))
            pairs.append(qa_pairs)
    return pairs
