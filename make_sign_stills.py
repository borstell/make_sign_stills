import cv2,sys,math,os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image

def hist(img):
	"""
	Returns a histogram analysis of a single image (in this case, a video frame)
	"""
	return cv2.calcHist([img],[0],None,[256],[0,256])

def read_frames(video):
	"""
	Reads a video file and returns a list of the histogram data for each frame
	"""
	v = cv2.VideoCapture(video)
	frames = []
	success,image = v.read()
	while success:
		success,image = v.read()
		if success:
			frames.append(hist(image))
	return frames

def get_frame_difference(video):
	"""
	Goes through the histograms of video frames pairwise and returns a list of 
	frame indices (x) and histogram differences (y)
	"""
	frames = read_frames(video)
	x = []
	y = []
	for n,f in enumerate(frames):
		if n!=len(frames)-1:
			x.append(n)
			y.append(1-(cv2.compareHist(hist(f),hist(frames[n+1]),cv2.HISTCMP_CORREL)))
	return x,y

def plot_changes(video):
	"""
	Returns a plot of the frame histogram differences over video frames
	(NB: not necessary for the analysis)
	"""
	plotname = video.split(".")[0]+"_plot_frames.png"
	x,y = get_frame_difference(video)
	fig, ax = plt.subplots()
	ax.plot(x, y)
	ax.set(xlabel='Frame', ylabel='Difference', title='Frame differences over time')
	ax.grid()

	fig.savefig(plotname)
	#plt.show()

def get_key_frames(video):
	"""
	Reads through the frame differences of a video, assumes the first peak to be the start of the sign,
	then returns the negative peaks (i.e. estimated holds) of the remaining frames
	"""
	x,y = get_frame_difference(video)
	diff = list(zip(y,x))
	peaks = signal.find_peaks_cwt(y,np.arange(1,15)) # These are hardcoded figures, you may need to adjust (e.g. 15,25)
	first = peaks[0]
	neg = [1-n for n in y[first:]]
	peaks2 = signal.find_peaks_cwt(neg,np.arange(1.5,8)) # These are hardcoded figures, you may need to adjust (e.g. 15,45)
	frames = [peak+first for peak in peaks2]
	return frames

def save_key_frames(video):
	"""
	Saves the frames that are estimated holds as image files and returns a list of their names
	(NB: only frames in the first half of the list of key frames are saved, as later frames are assumed 
	to constitute final rest position)
	"""
	outfile = video.split(".")[0]
	all_frames = get_key_frames(video)
	#frames = all_frames # Uncomment if you want all key frames to be included
	frames = all_frames[:math.ceil(len(all_frames)/2)] # Comment out if you want all key frames included
	count = 1
	filenames = []
	for f in frames:
		v = cv2.VideoCapture(video)
		v.set(1,f-1)
		ret,frame = v.read()
		filename = outfile+"_frame"+str(count)+".jpg"
		cv2.imwrite(filename,frame)
		filenames.append(filename)
		count += 1
	return filenames

def make_overlay(a,b,outname):
	"""
	Makes an overlay image of the key frames
	"""
	new_im = outname
	img1 = a
	img2 = b
	string = "convert %s %s -alpha set \
					-compose dissolve -define compose:args='25' \
					-gravity Center -composite %s" % (img2, img1, new_im)
	os.system(string)

def make_images(video):
	"""
	Creates overlay images of relevant key frames generated from videos and deletes individual frames
	"""
	imgs = save_key_frames(video)
	outname = imgs[0].split("_")[0]+"_still.jpg"
	if len(imgs) == 1:
		os.system("mv %s %s" % (imgs[0],outname))
	elif len(imgs) == 2:
		make_overlay(imgs[0],imgs[1],outname)
	elif len(imgs) >= 3:
		ims = imgs[:3]
		out1 = outname.split(".")[0]+"_A"+".jpg"
		make_overlay(ims[0],ims[1],out1)
		make_overlay(out1,ims[2],outname)
	if len(imgs) > 1:
		for img in imgs:
			os.system("rm "+img)		
	for f in os.listdir():
		if f.endswith("_A.jpg") or f.endswith("_B.jpg"):
			os.system("rm "+f)

def main():
	"""
	Iterates over files in directory and creates overlay images of key frames for each .mp4 file
	"""
	for f in os.listdir():
		if f.endswith(".mp4"):
			make_images(f)
			#plot_changes(f) # Uncomment if you want to create plots of changes in-between frames

if __name__=="__main__":
	main()
