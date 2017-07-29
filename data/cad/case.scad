include <bez.scad>
include <misc.scad>
$fa = 0.5;
$fs = 0.5;

thick = 2.2;
radius = 10;

box_w = 190;
box_l = 70;
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

module speaker()
{
    for(x=[0,speaker_s-m2thick])
        for(y=[0,speaker_s-m2thick])
            translate([x,y,0]) m2x4();
}

module pi()
{
    for(x=[0,lcd_w+m25thick])
        for(y=[0,lcd_h-m25thick])
            translate([x,y,0]) m25x6();
}

module pi_hole()
{
    translate([speaker_s+25+m25thick,thick,-10]) 
        translate([lcd_pad_left,lcd_pad_bottom,0])
            cube([lcd_w-(lcd_pad_left+lcd_pad_right),lcd_h-(lcd_pad_top+lcd_pad_bottom),20]);
}

difference()
{
    translate([box_w,0,0]) rotate([90,0,180]) union()
    {
        difference()
        {
            color([0.7,0.3,0.6]) translate([radius,radius,0]) hull()
            {
                cylinder(h=box_h,r=radius);
                translate([box_w-radius*2,0,0])
                    cylinder(h=box_h,r=radius);
                translate([-radius,0,0])
                    cube([box_w,box_l,box_h]);
            }
            translate([radius,thick,thick])
                cube([box_w-radius*2,box_l*2,box_h-thick*2]);
        }
        speaker_x = box_w-radius-(speaker_s+m2thick)/2+m2thick/2;
        translate([speaker_x-17,0,box_h]) ear();
        translate([speaker_x+17,0,box_h]) ear();
    }
    translate([0,14,0]) 
        pi_hole();
    translate([thick,thick,radius])
        cube([radius*2,box_h-thick*2,box_l*2]);
    translate([box_w-radius*2,thick,radius])
        cube([radius*2-thick,box_h-thick*2,box_l*2]);
    translate([radius+speaker_s/2,thick+10+speaker_s/2,5])
        scale([0.25, 0.25, 0.1])
            surface(file="cat.png",center=true,invert=true);
}
translate([radius,thick+10,thick]) speaker();
translate([speaker_s+25,thick+14,thick]) pi();
for(x=[thick,box_w-thick-m2thick])
    for(y=[thick,box_h-thick-m2thick])
        translate([x,y,radius])
            m2x5();
