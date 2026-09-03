import numpy as np
import cv2
from fella.fella_brain import FellaBrain
from fella.visual_cortex import VisualCortex

def test_visual_cortex():
    print("=========================================")
    print("PHASE 1: VISUAL CORTEX CROSS-MODAL BINDING")
    print("=========================================")
    
    # 1. Create dummy physical images (A Circle and a Square)
    circle_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(circle_img, (100, 100), 50, 255, -1)
    cv2.imwrite("test_circle.jpg", circle_img)

    square_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(square_img, (50, 50), (150, 150), 255, -1)
    cv2.imwrite("test_square.jpg", square_img)

    brain = FellaBrain(dim=256)
    v_cortex = VisualCortex(target_dim=256)

    # 2. Collapse the physical images into 256D Phase Signatures
    wave_circle = v_cortex.process_image("test_circle.jpg")
    wave_square = v_cortex.process_image("test_square.jpg")

    # 3. Manually inject the pure visual geometry into her matrix
    from fella.core_substrate import ENNNeuron
    brain.neurons["[V_CIRCLE]"] = ENNNeuron("[V_CIRCLE]", wave_circle)
    brain.matrix_keys.append("[V_CIRCLE]")
    brain.wave_matrix = np.vstack([brain.wave_matrix, wave_circle])

    brain.neurons["[V_SQUARE]"] = ENNNeuron("[V_SQUARE]", wave_square)
    brain.matrix_keys.append("[V_SQUARE]")
    brain.wave_matrix = np.vstack([brain.wave_matrix, wave_square])

    # 4. Prove Tabula Rasa before experiencing the images
    brain.get_or_create("circle")
    brain.get_or_create("square")
    
    print("\n[PRE-EXPERIENCE GEOMETRY]")
    print(f"Dot(text 'circle', visual image of circle) = {np.dot(brain.neurons['circle'].x_wave, wave_circle):.3f}")

    # 5. Experience the Cross-Modal Z-Events
    print("\n[INGESTING MULTI-MODAL Z-EVENTS...]")
    for _ in range(5):
        # We show her the image while speaking the words
        brain.record_event(["this", "is", "a", "circle", "[V_CIRCLE]"])
        brain.record_event(["this", "is", "a", "square", "[V_SQUARE]"])
        # Negative sample some noise
        brain.record_event(["dummy", "text", "event"])

    # 6. Prove Cross-Modal Binding (Gravity)
    print("\n[POST-EXPERIENCE GEOMETRY]")
    circle_match = np.dot(brain.neurons['circle'].x_wave, brain.neurons['[V_CIRCLE]'].x_wave)
    square_match = np.dot(brain.neurons['square'].x_wave, brain.neurons['[V_SQUARE]'].x_wave)
    confusion = np.dot(brain.neurons['circle'].x_wave, brain.neurons['[V_SQUARE]'].x_wave)
    
    print(f"Text 'circle' -> Visual Circle Gravity = {circle_match:.3f}")
    print(f"Text 'square' -> Visual Square Gravity = {square_match:.3f}")
    print(f"Text 'circle' -> Visual Square Gravity = {confusion:.3f}")
    
    if circle_match > confusion:
        print("\nSUCCESS: The physics engine successfully bound the physical geometry to the English text string!")

if __name__ == '__main__':
    test_visual_cortex()
