EXPORT_FIELD ?= substrate
PROJECT = microstrip_line

all: gerber2ems ems2s2p pybert

gerber2ems:
	gerber2ems -a --export-field=$(EXPORT_FIELD)

paraview:
	ems2paraview 0

ems2s2p:
	python3 ../ems2s2p.py ems/results/Port_0_data.csv -o $(PROJECT).s2p

generate_pybert_config:
	rm -f $(PROJECT).yaml
	cp ../pybert_config_template.yaml $(PROJECT).yaml
	echo "ch_file: $(PROJECT).s2p" >> $(PROJECT).yaml

pybert: generate_pybert_config
	pybert -c $(PROJECT).yaml

clean:
	rm -rf ems
	rm -f *.s2p

