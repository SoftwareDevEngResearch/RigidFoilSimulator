#include "udf.h"
#include "metric.h"
#include "mem.h"
#include "dynamesh_tools.h"
#include "math.h"

FILE*fp;
double current_time = 0.0000 ;
double vel[3]={0,0,0};/* define initial velocity*/
double omega[3]={0,0,0};/* define initial angular velocity*/
static real body_centroid[3]={0,0,0};
double Chord=0.15,F_density=1.225, Span=1.0; /*chold length, air density, span length (for 2D, span is one*/
double pi=3.1415926,frequency=1.6,Y_amplitude=0.075,w_amplitude=1.22173,U_flow=4; /*the frequency is physical frequency, Y_amplitude is heaving amplitude, w_amplitude is pitching amplitude, U_flow is flow velocity*/
double lift,drag,moment;
real NV_VEC( value_f ),NV_VEC( value_m );
real T_coordinate=0.0000;






DEFINE_CG_MOTION(Interface_out,dt,vel,omega,time,dtime)   
{
	double current_time = CURRENT_TIME;
	vel[1] = 2*pi*frequency*Y_amplitude*cos(2*pi*frequency*current_time+pi/2); 
}

DEFINE_CG_MOTION(Fluid_in,dt,vel,omega,time,dtime)     
{
	double current_time = CURRENT_TIME;
	vel[1] = 2*pi*frequency*Y_amplitude*cos(2*pi*frequency*current_time+pi/2); /*heaving velocity*/
	omega[2] =2*pi*frequency*w_amplitude*cos(2*pi*frequency*current_time);/*pitching velocity*/
}




DEFINE_CG_MOTION(Plate,dt,vel,omega,time,dtime) 
{
    double current_time = CURRENT_TIME;
	Domain * domain ;
	Thread * thread ;
	face_t  f;
	if (!Data_Valid_P ())
	return;
	thread=DT_THREAD(dt);    /*get the thread pointer for which this motion is defined */
	domain=THREAD_DOMAIN (thread);    /*pointer to face thread*/
	vel[1] = 2*pi*frequency*Y_amplitude*cos(2*pi*frequency*current_time+pi/2); 
	omega[2] =2*pi*frequency*w_amplitude*cos(2*pi*frequency*current_time);

	
	body_centroid[1]=DT_CG(dt)[1];/* reset the body centroid position in y direction*/
	Compute_Force_And_Moment(domain,thread,body_centroid,value_f,value_m,FALSE);

	lift=value_f[1]/(0.5*F_density*U_flow*U_flow*Chord*Span);			/* calculate the lift coefficient*/
	drag=value_f[0]/(0.5*F_density*U_flow*U_flow*Chord*Span);			/* calculate the drag coefficient*/
	moment=value_m[2]/(0.5*F_density*U_flow*U_flow*Chord*Chord*Span);		/*calculate the pitching moment coefficient*/
	
	
	fp=fopen("foil.dat", "a");												
	fprintf(fp, "%e,%e,%e\n",lift,drag,moment); 
	fclose(fp);

}
