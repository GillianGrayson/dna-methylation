import venn

labels = {'0001': 4,
          '0010': 3,
          '0011': 34,
          '0100': 2,
          '0101': 24,
          '0110': 23,
          '0111': 234,
          '1000': 1,
          '1001': 14,
          '1010': 13,
          '1011': 134,
          '1100': 12,
          '1101': 124,
          '1110': 123,
          '1111': 1234}
fig, ax = venn.venn4(labels, names=['list 1', 'list 2', 'list 3', 'list 4'])
fig.show()
fig.savefig('venn4_lib.png')
fig.savefig('venn4_lib.pdf')
