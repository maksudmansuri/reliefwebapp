from django.db import models
from accounts.models import HospitalDoctors, Hospitals, Labs, Pharmacy, Specailist
from patient.models import OrderBooking

class Campaign(models.Model):
    discount_type = models.CharField(max_length=6,
                                     choices=(('Amount', 'amount'), ('Rate', 'rate')),
                                     default="rate",
                                     null=False)
    discount_rate = models.IntegerField(null=True, blank=True)
    # discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # min_purchased_items = models.IntegerField( null=True, blank=True)
    # apply_to = models.CharField(max_length=20,
    #                             choices=(('Booking', 'Booking'), ('Hospitals', 'Hospitals'), ('HospitalDoctors', 'HospitalDoctors'), ('Labs', 'Labs'), ('Pharmacy', 'Pharmacy'), ('Specialist', 'Specialist')),
    #                             default="Specialist",
    #                             null=False)
                                
    # target_order = models.ForeignKey(OrderBooking, on_delete=models.SET_NULL, null=True, blank=True)
    target_specialist = models.ForeignKey(Specailist, related_name="dicount_specialist", on_delete=models.SET_NULL, null=True, blank=True)
    target_hospital = models.ForeignKey(Hospitals, related_name="dicount_hospital", on_delete=models.SET_NULL, null=True, blank=True)
    target_hospitaldoctor = models.ForeignKey(HospitalDoctors, related_name="dicount_hospitaldoctor", on_delete=models.SET_NULL, null=True, blank=True)
    target_lab = models.ForeignKey(Labs, related_name="dicount_lab", on_delete=models.SET_NULL, null=True, blank=True)
    target_pharmacy = models.ForeignKey(Pharmacy, related_name="dicount_pharmacy", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {}".format(self.discount_type,
                                                                   self.discount_rate,
                                                                #    self.discount_amount,
                                                                #    self.min_purchased_items,
                                                                #    self.apply_to,
                                                                   self.target_specialist,
                                                                   self.target_hospital,
                                                                   self.target_hospitaldoctor,
                                                                   self.target_lab,
                                                                   self.target_pharmacy,
                                                                #    self.target_orderss,
                                                                   self.created_at,
                                                                   self.updated_at)


class Coupon(models.Model):
    minimum_cart_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount_rate = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.minimum_cart_amount,
                                          self.discount_rate,
                                          self.created_at,
                                          self.updated_at)
