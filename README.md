# Socket-Programming

To create an application level file sharing protocol with support for download and upload for files and indexed searching.

Features:
----

1.  The system should have 2 clients (acting as servers simultaniously) listening to the communication channel for requests and waiting to share files (avoiding collisions) using an application layer protocol (like FTP/HTTP).

2.  Each client has the ability to do the following: a. Know the files present on each other machines in the designated shared folders. b. Download the files from the shared folder

3.  The system should perodically check for any changes made to the shared folders.

4.  File transfer should incorporate MD5checksums to handle file transfer errors.

Specifications
----
The system should incorporate the following commands:

IndexGet: Request to display the files in the shared folder which is assumed to be the same directory as the code.

Flags : shortlist, longlist

FileHash: Indicates that the client wants to check if any of the files on the other end have been changed.

Flags: verify, checkall

FileDownload: Used to download the files from the shared folder of connected users. In case no flag is mentioned TCP is considered as default.

Flags: TCP,UDP

The given project is done in Python 2.For more details refer to Report.pdf
