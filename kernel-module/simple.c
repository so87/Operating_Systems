#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/types.h>
#include <linux/slab.h>

struct birthday {
	int day;
	int month;
	int year;
	struct list_head list;
};

static LIST_HEAD(birthday_list);

int simple_init(void)
{
    printk(KERN_INFO "Loading Module\n");
	struct birthday *person;
	person = kmalloc(sizeof(*person), GFP_KERNEL);
	person->day = 2;
	person->month = 8;
	person->year = 1995;

	// Create List
	INIT_LIST_HEAD(&person->list);
	list_add_tail(&person->list, &birthday_list);

	// Make 5 birthday elements
	struct birthday *person2, *person3, *person4, *person5;
	person2 = kmalloc(sizeof(*person2), GFP_KERNEL);
	person3 = kmalloc(sizeof(*person3), GFP_KERNEL);
	person4 = kmalloc(sizeof(*person4), GFP_KERNEL);
	person5 = kmalloc(sizeof(*person5), GFP_KERNEL);

	person2->day = 5;
	person2->month = 5;
	person2->year = 1980;
	list_add_tail(&person2->list, &birthday_list);

	person3->day = 7;
	person3->month = 7;
	person3->year = 1970;
	list_add_tail(&person3->list, &birthday_list);

	person4->day = 20;
	person4->month = 20;
	person4->year = 1960;
	list_add_tail(&person4->list, &birthday_list);	

	person5->day = 30;
	person5->month = 1;
	person5->year = 1999;
	list_add_tail(&person5->list, &birthday_list);

	// Make pointers to iterate through the list
	struct birthday *ptr, *next;
	
	// Print them to the kernel buffer log
	list_for_each_entry(ptr, &birthday_list, list){
	printk("Printing A Birthday");
	printk("DAY: %d\n", ptr->day);
	printk("MONTH: %d\n", ptr->month);
	printk("YEAR: %d\n", ptr->year);
	}

	/* This function is called when the module is loaded. */
    return 0;
}

/* This function is called when the module is removed. */
void simple_exit(void) {
	printk(KERN_INFO "Removing Module\n");

	// Make pointers to iterate through the list
	struct birthday *ptr, *next;

	// Delete elements in list and free memory
	list_for_each_entry_safe(ptr, next, &birthday_list, list){
		list_del(&ptr->list);
		kfree(ptr);
	}

}

/* Macros for registering module entry and exit points. */
module_init( simple_init );
module_exit( simple_exit );

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Simple Module");
MODULE_AUTHOR("SGG");
