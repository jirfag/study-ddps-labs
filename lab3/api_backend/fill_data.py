from api_backend.models import Image, Tag

user_id = 5

Tag.objects.all().delete()
Tag.objects.create(name='Cat', desc='Cat (animal)')
Tag.objects.create(name='Animal', desc='Tag for all animals')
Tag.objects.create(name='Computer', desc='All related to computers')
Tag.objects.create(name='Car', desc='Different car models')
Tag.objects.create(name='MercedesBenz', desc='All produced by MercedesBenz')
Tag.objects.create(name='BMW', desc='All produced by BMW')
Tag.objects.create(name='Night', desc='Photos at the night')
Tag.objects.create(name='Sky', desc='Photos with the sky')
Tag.objects.create(name='Cute', desc='Something cute')
Tag.objects.create(name='Water', desc='Photos with the water')
Tag.objects.create(name='Nature', desc='Photos with the nature')

Image.objects.all().delete()
def add_img(name, desc, source, tag_names):
    img = Image.objects.create(name=name, desc=desc, source=source, owner_id=user_id)
    for tag_name in tag_names:
        img.tags.add(Tag.objects.get(name=tag_name))

add_img('some duck', 'some yellow duck in the water', 'http://web.stanford.edu/dept/CTL/cgi-bin/academicskillscoaching/wp-content/uploads/2012/07/baby-duck.jpg', ['Animal', 'Water', 'Cute'])
add_img('kitten', 'ginger kitten', 'http://cf.ltkcdn.net/cats/images/std/159706-357x421-kitten.jpg', ['Animal', 'Cat', 'Cute'])
add_img('mercedes benz sl r231', 'cool car', 'http://www.mercedes-benz.ca/content/media_library/hq/hq_mpc_reference_site/passenger_cars_ng/new_cars/models/sl-class/r231/model_navigation_library/mercedes-benz_sl-class_r231_model_navigation_960x298_12-2011_jpg.object-Single-MEDIA.tmp/mercedes-benz_sl-class_r231_model_navigation_960x298_12-2011.jpg', ['Car', 'MercedesBenz'])
add_img('field', 'some field', 'http://wallpaperscraft.com/image/45608/3840x2160.jpg', ['Sky', 'Nature'])
add_img('night city', 'some city', 'http://p1.pichost.me/640/39/1629941.jpg', ['Night', 'Sky'])
add_img('bmw m9', 'm9 concept', 'http://www.bmwblog.com/wp-content/uploads/bmw-m9.png', ['Car', 'BMW'])
