include <util.scad>
$fa = 0.5;
$fs = 0.5;

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
    translate([pi_x+m25thick,thick,-10]) 
        translate([lcd_pad_left,lcd_pad_bottom,0])
            cube([lcd_w-(lcd_pad_left+lcd_pad_right),lcd_h-(lcd_pad_top+lcd_pad_bottom),20]);
}

pi_h = 19;
pi_x = speaker_s+25;
speaker_h = thick+13;
speaker_x = radius+5;

difference()
{
    union()
    {
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
                speaker_pad = box_w-speaker_x-(speaker_s+m2thick)/2+m2thick/2;
                translate([speaker_pad-17,0,box_h]) ear();
                translate([speaker_pad+17,0,box_h]) ear();
            }
            translate([0,pi_h,0]) 
                pi_hole();
            translate([thick,thick,radius])
                cube([radius*2,box_h-thick*2,box_l*2]);
            translate([box_w-radius*2,thick,radius])
                cube([radius*2-thick,box_h-thick*2,box_l*2]);
            translate([speaker_x+speaker_s/2,speaker_h+speaker_s/2,5])
                scale([0.30, 0.30, 0.1])
                    surface(file="cat.png",center=true,invert=true);
        }
        translate([speaker_x,speaker_h,thick]) speaker();
        translate([pi_x,thick+pi_h,thick]) pi();
        for(x=[thick,box_w-thick-m25thick])
            for(y=[thick,box_h-thick-m25thick])
                translate([x,y,radius])
                    m25xBox_l();
    }
    // trimmings
    for(x=[thick+m25thick+0.5,pi_x+m25thick-0.8])
        translate([x,thick,thick])
            cube([3,box_h-thick*2,10]);
}
