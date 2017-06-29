import os

for chap in xrange(1,26+1):
    folder = '%02d_chapter_notes' % chap
    content = ['chapter %02d: ()\n' % chap]
    for section in range(1,8):
        content.append('%02d.%d: -----\n' % (chap, section))
    content.append('problems\n')
    content.append(('%02d.00, ' % chap)*3 + '[,,]' +'\n')
    print(chap)
    os.mkdir(folder)
    notes = open(folder+'/notes.txt', 'w')
    notes.write(''.join(content))
    notes.close()
    scratch = open(folder+'/scratch.py', 'w')
    scratch.close()
