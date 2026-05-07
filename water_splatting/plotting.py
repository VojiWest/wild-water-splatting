import matplotlib.pyplot as plt

def plot_loss(train_losses, title=""):
    train_losses_ma = []
    for idx, loss in enumerate(train_losses):
        window = train_losses[max(idx-24, 0):idx+1]
        avg = sum(window)/len(window)
        train_losses_ma.append(avg)
    
    plt.plot(train_losses_ma)
    plt.ylabel("Loss")
    plt.xlabel("Iteration")
    plt.title(title)
    save_name = title + "_" + "loss_plot.png"
    plt.savefig(save_name)