include <bez.scad>
$fa = 0.5;
$fs = 0.5;

thick = 2.2;
radius = 10;

box_w = 190;
box_l = 60;
box_h = 81;

lcd_w = 84.96;
lcd_h = 56.52;
lcd_pad_left = 7.1;
lcd_pad_right = 1.9;
lcd_pad_top = 1.9;
lcd_pad_bottom = 2.1;

tft_w = 91.19;
tft_h = 49.91;

m25thick = lcd_h-tft_h;
m2thick = 5;

speaker_s = 52+m2thick;

module m25x6()
{
    mount(s=m25thick,h=5,d=2.5,depth=5);
}

module m2x4()
{
    mount(s=m2thick,h=4,d=2,depth=4,cylinder=true);
}

module m25xBox_l()
{
    mount(s=m25thick,h=box_l,d=2.5,depth=5);
}

module mount(s,h,d,depth,cylinder=false)
{
    translate([s/2,s/2,h/2]) difference()
    {
        if(cylinder)
        {
            cylinder(d=s,h=h,center=true);
        }
        else
        {
            cube([s,s,h],center=true);
        }
        translate([0,0,h/2-depth+0.1]) cylinder(h=depth,d=d-0.1);
    }
}

module ear(ear_l=7)
{
    translate([0,ear_l/2,-0.1]) difference()
    {
        color([0.3,0.5,0.7]) hull()
        {
            translate([0,0,15])
                scale([1.5,1,1])
                    sphere(2,center=true);
            cube([20,ear_l,0.5],center=true);
        }
        translate([0,0,-1]) cube([21,ear_l+7,2],center=true);
    }
}

module cat_whisker(length,width,right_align=false)
{
    hull()
    {
        translate([0,0,0]) cylinder(d=width,h=10,center=true);
        if(right_align)
        {
            translate([length,0,0]) cylinder(d=width,h=10,center=true);
        }
        else
        {
            translate([-length,0,0]) cylinder(d=width,h=10,center=true);
        }
    }
}
