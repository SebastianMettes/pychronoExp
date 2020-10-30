#test
import pychrono as chrono
my_vect1 = chrono.ChVectorD()
my_vect1.x = 5
my_vect1.y = 2
my_vect1.z = 3

my_vect2 = chrono.ChVectorD(3,4,5)

my_vect4 = my_vect1*10 + my_vect2

my_len = my_vect4.Length()

print('vector length =', my_len)

my_quat = chrono.ChQuaternionD(1,2,3,4)
my_qconjugate = ~my_quat
print ('quat. conjugate  =', my_qconjugate)
print ('quat. dot product=', my_qconjugate ^ my_quat)
print ('quat. product=',     my_qconjugate % my_quat)
my_vec = chrono.ChVectorD(1,2,3)
my_vec_rot = my_quat.Rotate(my_vec)


