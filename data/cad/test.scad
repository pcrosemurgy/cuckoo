$fa = 0.5;
$fs = 0.5;

thick = 2.2;
radius = 10;

box_w = 190;
box_l = 60;
box_h = 75;

lcd_w = 84.96;
lcd_h = 56.52;
lcd_pad_left = 7.1;
lcd_pad_right = 1.9;
lcd_pad_top = 1.9;
lcd_pad_bottom = 1.9;

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

module pi()
{
    for(x=[0,lcd_w+m25thick])
        for(y=[0,lcd_h-m25thick])
            translate([x,y,thick]) m25x6();
}

module pi_hole()
{
    translate([speaker_s+25+m25thick,thick,-10]) 
        translate([lcd_pad_left,lcd_pad_bottom,0])
            cube([lcd_w-(lcd_pad_left+lcd_pad_right),lcd_h-(lcd_pad_top+lcd_pad_bottom),20]);
}

module speaker()
{
    difference()
    { 
        color([0.7,0.3,0.5]) cube([speaker_s,speaker_s,thick]);
        translate([speaker_s/2,speaker_s/2,0]) cat_cutout();
    }
    for(x=[0,speaker_s-m2thick])
        for(y=[0,speaker_s-m2thick])
            translate([x,y,thick]) m2x4();
}

module cat_cutout()
{
    hull()
    {
        translate([-5,3,0]) cylinder(r=2,h=10,center=true);
        translate([5,3,0]) cylinder(r=2,h=10,center=true);
        translate([0,-2,0]) cylinder(r=4,h=10,center=true);
    }
    translate([9.5,4,0])
        rotate([0,0,10])
            cat_whisker(length=15,width=1.3,right_align=true);
    translate([-9.5,4,0])
        rotate([0,0,-10])
            cat_whisker(length=15,width=1.3,right_align=false);
    translate([8.9,1,0])
        rotate([0,0,0])
            cat_whisker(length=15,width=1.3,right_align=true);
    translate([-8.9,1,0])
        rotate([0,0,-0])
            cat_whisker(length=15,width=1.3,right_align=false);
    translate([7.5,-2,0])
        rotate([0,0,-10])
            cat_whisker(length=15,width=1.3,right_align=true);
    translate([-7.5,-2,0])
        rotate([0,0,10])
            cat_whisker(length=15,width=1.3,right_align=false);
    translate([-7,10,0]) cat_eye();
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

module cat_eye()
{
    scale([1,2,1]) intersection()
    {
        translate([0,-2,0]) cylinder(d=7,h=10);
        translate([0,2,0]) cylinder(d=7,h=10);
    }
}

!cat_cutout();
!speaker();
translate([speaker_s+25,thick,0]) pi();
difference()
{
    translate([-5,-5,0])
        color([0.2,0.5,0.8]) 
            cube([185,75,thick]);
    pi_hole();
}
