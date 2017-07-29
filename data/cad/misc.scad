include <bez.scad>

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
p0 = [0, 5];
p1 = [4, 0];
p2 = [8, 0];
p3 = [12, 5];
translate([speaker_s/2/20+3,speaker_s/2/20+8,-10]) linear_extrude(height=20) polyline(bezier_curve(0.05,p0,p1,p2,p3),1.5);
translate([speaker_s/2/20-6-13,speaker_s/2/20+8,-10]) linear_extrude(height=20) polyline(bezier_curve(0.05,p0,p1,p2,p3),1.5);
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
