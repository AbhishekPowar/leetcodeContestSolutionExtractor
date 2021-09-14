def filterPythonFiles():
    with open('finalData.json','r') as f:
            s=f.read()

    import json
    js = json.loads(s)

    indices =[]
    country =set()
    for idx, obj in enumerate(js):
            lang = obj['question_ids'][0]['lang']
            if 'python3' in lang: 
                    indices.append(obj)
    s = json.dumps(indices,indent=4)
    with open('python.json','w') as f:
            f.write(s)

def createFileForQuestion():
    with open('python.json','r') as f:
            s=f.read()

    import json
    js = json.loads(s)

    for qn in range(0,4):
        with open(f'python_{qn}.py','w') as f:
            out=''
            for idx,j in enumerate(js):
                out+= j['question_ids'][qn]['code']
                out+= f'\n#------------------------{idx}-------------------------------\n' 
            f.write(out)

if __name__ == "__main__":
    filterPythonFiles()
    createFileForQuestion()
