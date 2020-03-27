from intelhex import IntelHex
import sys

ih = IntelHex() 
ih.fromfile(sys.argv[1],format='hex')
program_dict = ih.todict()

max_program_size = 8192
program_size     = len(program_dict)
memory_per_cent	 = round((program_size * 100)/max_program_size, 2)

print("O programa usa " + str(program_size) + str(' bytes (') + str(memory_per_cent) + "%) de armazenamento. O máximo são " +str(max_program_size) + str(" bytes."))

program_dict = sorted(program_dict.items(), key=lambda kv: kv[0])

program = []
for i in program_dict:
    program.append(hex(i[1]) + str(", "))

program = "".join(program)
print(program)