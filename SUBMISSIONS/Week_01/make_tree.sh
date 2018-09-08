
#!/bin/bash
mkdir Week_01
cd Week_01
mkdir s1
cd s1
mkdir s2
mkdir s3
cd s3
touch conf.txt
cd ../s2
touch text_chunk1.txt
mkdir Advanced
cd Advanced/
touch text_chunk2.txt
cd ..
cd ../s3
echo "I love bash scripting." >> conf.txt
cd ../s2
echo "A whole new world" >> text_chunk1.txt
echo "A new fantastic point of view" >> text_chunk1.txt
cd Advanced/
cat ../text_chunk1.txt > text_chunk2.txt
echo "Do you want to build a snowman?" >> text_chunk2.txt

