def readFile(filePath):
    vertices = []
    indices = []
    
    with open(filePath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('v '):
                parts = line.split()
                if("" in parts):
                    parts.remove('')
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.split()
                if("" in parts):
                    parts.remove('')
                parts[1] = parts[1].split('/')[0]
                parts[2] = parts[2].split('/')[0]
                parts[3] = parts[3].split('/')[0]
                indices.append([int(parts[1]), int(parts[2]), int(parts[3])])    
                if len(parts) == 5:
                    parts[4] = parts[4].split('/')[0]
                    indices.append([int(parts[2]), int(parts[3]), int(parts[4])])
                        
    return vertices, indices

if(__name__ == "__main__"):
    vertices, indices = readFile("./app/assets/scene.obj")
    vertices_string = " ".join([f"{v[0]} {v[1]} {v[2]}" for v in vertices])
    indices_string = " ".join([f"{i[0]} {i[1]} {i[2]}" for i in indices])
    colors_string = " ".join([f"{0} {0} {0} {0}" for i in indices])


    #print("Vertices: ", vertices_string)
    #print("Indices: ", indices_string)
    # write to file
    with open("./app/assets/vertices.txt", "w") as f:
        f.write(vertices_string)
    with open("./app/assets/indices.txt", "w") as f:
        f.write(indices_string)
    with open("./app/assets/colors.txt", "w") as f:
        f.write(colors_string)