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

m25thick = lcd_h-tft_h;

module m25x6()
{
    mount(s=m25thick,h=5,d=2.4,depth=5);
}

module mount(s,h,d,depth)
{
    translate([s/2,s/2,h/2]) difference()
    {
        cube([s,s,h],center=true);
        translate([0,0,h/2-depth+0.1]) cylinder(h=depth,d=d-0.1);
    }
}

module piBase()
{
    pad = m25thick*2;
    difference()
    {
        cube([lcd_w+pad,lcd_h+thick*2,thick]);
        translate([pad/2,thick,-10]) cube([lcd_w,lcd_h,20]);
    }
    translate([pad/2-m25thick,thick,thick]) m25x6();
    translate([pad/2+lcd_w,thick,thick]) m25x6();
    translate([pad/2-m25thick,thick+lcd_h-m25thick,thick]) m25x6();
    translate([pad/2+lcd_w,thick+lcd_h-m25thick,thick]) m25x6();
}

module speakerBase()
{
    
}

//!piBase();
!speakerBase();
