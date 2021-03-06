from car_dataset import *
from network import *
from config import Config


def predict(model):
    predictions = []
    test_loader = DataLoader(dataset=test_dataset, batch_size=4, shuffle=False, num_workers=4)
    model.eval()

    for img, _, _ in tqdm(test_loader):
        with torch.no_grad():
            output = model(img.to(Config.device))
        output = output.data.cpu().numpy()
        for out in output:
            coords = extract_coords(out)
            s = coords2str(coords)
            predictions.append(s)

    test = pd.read_csv(Config.DATA_PATH + 'sample_submission.csv')
    test['PredictionString'] = predictions
    test.to_csv(str(Config.expriment_id) + '_predictions.csv', index=False)
