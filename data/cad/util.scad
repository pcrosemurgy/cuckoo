$fa = 0.5;
$fs = 0.5;

thick = 5;
radius = 10;

box_w = 190;
box_l = 60;
box_h = 75;

lcd_w = 84.96;
lcd_h = 56.52;

tft_w = 91.19;
tft_h = 49.91;

speaker_r = 28;

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

union()
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
            cube([box_w-radius-thick,box_l*1.1,box_h-thick*2]);
    }
    speaker_x = box_w-radius-speaker_r-thick/2;
    translate([speaker_x-17,0,box_h]) ear();
    translate([speaker_x+17,0,box_h]) ear();
    speaker(speaker_x,radius,box_h-thick-speaker_r);
}

module M25x6()
{
    mount(s=tft_w-lcd_w,h=10,d=2.4,depth=6);
}

module mount(s,h,d,depth)
{
    difference()
    {
        %cube([s,s,h],center=true);
        #translate([0,0,h/2-depth]) cylinder(h=depth+0.1,d=d-0.1);
    }
}

!M25x6();

module tft(x,y,z,positive=true)
{
    if(positive)
    {
        difference()
        {
            translate([x,y,z])
                cube([tft_w,radius+thick,tft_h+4]);
            tft_mount(x+(tft_w-lcd_w)/2,y,z-2,false);
        }
    }
    else
    {
        translate([x,y,z])
            cube([lcd_w,radius*2,tft_h]);
    }
}

module speaker(x,y,z)
{
    translate([x,y,z])
        rotate([90,0,0])
            color([0.8,0.2,0.4])
                cylinder(h=radius,r=speaker_r);
}
