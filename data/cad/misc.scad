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

module m2x5()
{
    mount(s=m2thick,h=box_l-thick,d=2,depth=5);
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
