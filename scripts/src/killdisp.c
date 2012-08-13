#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
// killdisp script for external monitors, part of thinkdisp
// we want this compiled because we'll eventually use setuid for no
// password prompt

void main()
{
    printf("WARNING: must run as root, else you'll get a segfault\n");
    printf("turning off display\n");
    system("xrandr --output VIRTUAL --off");
    
    printf("killing screenclone\n");
    system("pkill screenclone");
    
    printf("killing X server...\n");
    printf("running X servers are:\n");

    //print running X servers
    FILE *fp;
    fp = popen("pgrep X", "r");
    char line[200];
    fgets(line, sizeof line, fp);
    printf("%s", line);
    pclose(fp);


    //get # running X servers
    FILE *fp2;
    fp2 = popen("pgrep -c X", "r");
    char line2[200];
    fgets(line2, sizeof line2, fp2);
    printf("%s", line2);
    pclose(fp2);

    int count = atoi(line2);
    printf("%d", count);

    //if more than one X server, kill the latest one
    if (count > 1) {
        system("sudo kill $(pgrep -n X)");
        sleep(3);
    }
   
    //insert bbswitch and shut off the nvidia card 
    system("sudo rmmod nvidia");
    sleep(1);
    system("sudo modprobe bbswitch");
    //write OFF to bbswitch
    FILE *bbswitch;
    bbswitch = fopen("/proc/acpi/bbswitch", "w");
    fprintf(bbswitch, "OFF");
    fclose(bbswitch);

}
