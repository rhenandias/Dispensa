from intelhex import IntelHex
import sys

ih = IntelHex() 
ih.fromfile(sys.argv[1],format='hex')
program_dict = ih.todict()

print("Tamanho do programa: " + str(len(program_dict)) + str(' bytes'))

program_dict = sorted(program_dict.items(), key=lambda kv: kv[0])

for i in program_dict:
    print (i[0], hex(i[1]))

program = []
for i in program_dict:
    program.append(hex(i[1]) + str(", "))


program = "".join(program)
print(program)