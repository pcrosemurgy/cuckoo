include <util.scad>
$fa = 0.5;
$fs = 0.5;

module letter()
{
    pad = 20;
    polyline(bezier_curve(0.05,[0,0],[0,0.7*pad],[pad,0.7*pad],[pad,0]),1);
    for(x=[0,pad])
        polyline(bezier_curve(0.05,[x,-20],[x,-20],[x,0],[x,0]),1);
}

module anna()
{
    for(x=[10,115])
        translate([x,-6,5]) 
            cylinder(h=10,d=5);
    for(x=[0:3])
        translate([x*35,0,0]) 
            linear_extrude(height=20) letter();
}

translate([0,0,0]) difference()
{
    translate([1.5,1.5,0])
        color([0.3,0.5,0.6]) 
            cube([box_w-3,box_h-3,thick]);
    for(x=[thick+m25thick/2,box_w-(thick+m25thick/2)])
        for(y=[thick+m25thick/2,box_h-(thick+m25thick/2)])
            translate([x,y,-1]) cylinder(h=10,d=2);
    translate([32,box_h/2+5,-10]) 
        anna();
    translate([41.5,0,-10]) linear_extrude(height=20) 
        polyline(bezier_curve(0.05,[0,0],[0,0],[0,5],[0,5]),4);
}
