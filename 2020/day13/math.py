# def MMI(A, n, s=1, t=0, N=0):
# 	# result = (n < 2 and t%N or MMI(n, A%n, t, s-A//n*t, N or n),-1)
# 	if n == 0:
# 		return -1
# 	else:
# 		part1 = n < 2

# 		if N > 0:
# 			part2 = t%N
# 		else:
# 			part2 = False
	
# 		part3 = MMI(
# 			n, 
# 			A%n, 
# 			t, 
# 			s-A//n*t, 
# 			N or n
# 		)

# 		print(A, n, part1, part2, part3)
# 		print(part1 and part2 or part3)
# 		return part1 and part2 or part3
# 	# return result[is_done]

# mmi = MMI(7, 13)
# print(mmi)

# mmi = MMI(3, 368)
# print(mmi)

# abc = [1, 6, 4, 5, 7]
# k = 4
# print(abc[False])

print(pow(13, -1, 7))