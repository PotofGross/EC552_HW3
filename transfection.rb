class Protocol
    def main
      operations.retrieve  # locate required items and display instructions to get them
      operations.make      # create items for the outputs
  
      operations.each do |operation|
        operation_task(operation)
      end
  
      operations.store    # move everything where it belongs
    end
  
    # Perform the Streak Plate protocol for a single operation
    #
    # @param operation [Operation] the operation to be executed
    def operation_task(operation)
      # Declare references to input/output objects
      dmem = operation.input('dmem').item
      optimem = operation.input('optimem').item
      lipofectamine = operation.input('lipofectamine').item
      output_plate = operation.output('plate').item
      co2_incub = operation.output('co2_incub').item
      # Display cell seeding instructions
      show do
        title 'Plate Cells'
        check "Get a 24-well plate and label it #{output_plate.id}"
        check 'Trypsinize and count the cells'
        check "Plate 0.5 -1.25x10\^5 cells per well in 0.5 ml of complete growth medium #{dmem.id}. Cell density should be 50-80\% confluent on the day of transfection"
        check '(Optional) Remove growth medium from cells and replace with 0.5 ml of complete growth medium'
      end
  
      show do
          title 'Dilute DNA in Opti-Mem Media'
          check "For each well, dilute 0.5 g of DNA in 100 l of Opti-MEM I Reduced Serum Media without serum #{optimem}"
      end
  
      show do
          title 'Add Lipofectamine'
          check "Add 0.75-1.75 l Lipofectamine #{lipofectamine.id} to each well in the plate #{output_plate.id} containing diluted DNA-Opti-MEM solution"
          check 'Mix gently'
          check 'Uncubate 30 minutes at room temperature to form DNA- Lipofectamine LTX Reagent complexes.'
      end
  
      show do 
          title 'Add DNA-Lipofectamine complexes'
          check "Add 100 l of the DNA- Lipofectamine LTX Reagent complexes to each well in the plate #{output_plate.id}" 
          check 'Mix gently by rocking the plate back and forth.'
      end
  
      show do
          title 'Incubate cells'
          check "Incubate in CO2 incubator #{co2_incub.id} at 37 C"
          check 'Wait 18-24 hours before assaying for transgene expression'
      end
      # Move the plate to the incubator
      output_plate.move('CO2 incubator')
    end
  end
  