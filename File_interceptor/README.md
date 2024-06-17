This code implements file interceptor. This means the file type in code is replaced by any download link determined by the hacker.

This code is tested on the website "http://www.surfoffline.com/". 
IMPORTANT: This code does not apply HSTS Hijack. Therefore, It cannot bypass HTTPS. HSTS Hijack will be available later on on this repository.

Parameters are hard coded inside the code. You can change FileType and target_link parameters as you wish. QueueNumb can also be changed.
Important thing is the fact that it would be better if FileType and the extension of the file downloaded from target_link are the same to fool the victim.

This code was tested on Kali Linux. I am not sure whether this code works on MacOs or not.
To run tpye "python3 fi.py".

