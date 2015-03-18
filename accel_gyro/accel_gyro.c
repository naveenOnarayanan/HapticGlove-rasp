#include <unistd.h>
#include <math.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include "sensor.c"
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <arpa/inet.h>
#include <stdarg.h>
#include <errno.h>

#define DT 0.5 // [s/loop] loop period. 20ms
#define AA 0.97         // complementary filter constant

#define A_GAIN 0.0573      // [deg/LSB]
#define G_GAIN 0.070     // [deg/s/LSB]
#define RAD_TO_DEG 57.29578
#define M_PI 3.14159265358979323846
#define SERVER_PORT 3002
unsigned char buffer[1500];
int clientSocketId;

void sendData(double x, double y) {
	struct sockaddr_in connectionSocketAddress;

	memset(&connectionSocketAddress, 0, sizeof(connectionSocketAddress));

	connectionSocketAddress.sin_family = AF_INET;
	connectionSocketAddress.sin_addr.s_addr = inet_addr("0.0.0.0");
	connectionSocketAddress.sin_port = htons(SERVER_PORT);

	sprintf(buffer, "{ \"accel_gyro\": {\"x\": %7.3f, \"y\": %7.3f}}\0", x, y);
        printf("%d\n", strlen(buffer));
	sendto(clientSocketId, buffer, strlen(buffer), 0, (struct sockaddr *)&connectionSocketAddress, sizeof(connectionSocketAddress));

}

void  INThandler(int sig)
{
        signal(sig, SIG_IGN);
        exit(0);
}

int mymillis()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec) * 1000 + (tv.tv_usec)/1000;
}

int timeval_subtract(struct timeval *result, struct timeval *t2, struct timeval *t1)
{
    long int diff = (t2->tv_usec + 1000000 * t2->tv_sec) - (t1->tv_usec + 1000000 * t1->tv_sec);
    result->tv_sec = diff / 1000000;
    result->tv_usec = diff % 1000000;
    return (diff<0);
}

int main(int argc, char *argv[])
{

        clientSocketId = socket(AF_INET, SOCK_DGRAM, 0);
        if (clientSocketId < 0) {
            printf("Failed opening socket\n");
            exit(EXIT_FAILURE);
        }

	float rate_gyr_y = 0.0;   // [deg/s]
	float rate_gyr_x = 0.0;    // [deg/s]
	float rate_gyr_z = 0.0;     // [deg/s]

	int  acc_raw[3];
	int  mag_raw[3];
	int  gyr_raw[3];

	float gyroXangle = 0.0;
	float gyroYangle = 0.0;
	float gyroZangle = 0.0;
	float AccYangle = 0.0;
	float AccXangle = 0.0;
	float CFangleX = 0.0;
	float CFangleY = 0.0;

	int startInt  = mymillis();
	struct  timeval tvBegin, tvEnd,tvDiff;

	signed int acc_y = 0;
	signed int acc_x = 0;
	signed int acc_z = 0;
	signed int gyr_x = 0;
	signed int gyr_y = 0;
	signed int gyr_z = 0;

        signal(SIGINT, INThandler);

	enableIMU();

	gettimeofday(&tvBegin, NULL);

	while(1)
	{
	startInt = mymillis();

	//read ACC and GYR data
	readACC(acc_raw);
	readGYR(gyr_raw);

	//Convert Gyro raw to degrees per second
	rate_gyr_x = (float) gyr_raw[0] * G_GAIN;
	rate_gyr_y = (float) gyr_raw[1]  * G_GAIN;
	rate_gyr_z = (float) gyr_raw[2]  * G_GAIN;

	//Calculate the angles from the gyro
	gyroXangle+=rate_gyr_x*DT;
	gyroYangle+=rate_gyr_y*DT;
	gyroZangle+=rate_gyr_z*DT;

	//Convert Accelerometer values to degrees
	AccXangle = (float) (atan2(acc_raw[1],acc_raw[2])+M_PI)*RAD_TO_DEG;
	AccYangle = (float) (atan2(acc_raw[2],acc_raw[0])+M_PI)*RAD_TO_DEG;

        //Change the rotation value of the accelerometer to -/+ 180 and move the Y axis '0' point to up.
        //Two different pieces of code are used depending on how your IMU is mounted.
        //If IMU is upside down
	/*
        if (AccXangle >180)
                AccXangle -= (float)360.0;

        AccYangle-=90;
        if (AccYangle >180)
                AccYangle -= (float)360.0;
	*/

        //If IMU is up the correct way, use these lines
        AccXangle -= (float)180.0;
	if (AccYangle > 90)
	        AccYangle -= (float)270;
	else
		AccYangle += (float)90;


	//Complementary filter used to combine the accelerometer and gyro values.
	CFangleX=AA*(CFangleX+rate_gyr_x*DT) +(1 - AA) * AccXangle;
	CFangleY=AA*(CFangleY+rate_gyr_y*DT) +(1 - AA) * AccYangle;


	//printf ("CFangleX %7.3f CFangleY %7.3f\n",CFangleX,CFangleY);
        printf("cfangle_x: %7.3f cfangle_y: %7.3f \n", CFangleX, CFangleY);                                                                                                                                                                                                                                                                                                   

	//Each loop should be at least 20ms.
        while(mymillis() - startInt < (DT*1000))
        {
            usleep(100);
        }

        printf("Sending..\n");
        sendData(CFangleX, CFangleY);

    }
}

