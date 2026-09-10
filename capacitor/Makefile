help:
	@echo - make start
	@echo - make paraview
	@echo - make clear

start:
	gerber2ems -a --export-field=substrate

paraview:
	ems2paraview 0

png:
	ems2png

clear:
	rm -r ems
	rm -r simulation_images
