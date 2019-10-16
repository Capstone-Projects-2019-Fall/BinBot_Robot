public interface Treads{


    /**
     * <h1>patrol()</h1>
     * This method is used to allow BinBot to move a set amount of distance.
     * Calling this method will instruct BinBot to travel a set distance
     * in its search for waste objects.
     *
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public void patrol();


    /**
     * <h1>forward()</h1>
     * This method is used to invoke the treads on BinBot. Calling this method
     * will make BinBot move in a forward direction.
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public void forward();


    /**
     * <h1>leftTurn()</h1>
     * This method is used to invoked the treads on BinBot. Calling this
     * method will make BinBot's treads make a left turn
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public void leftTurn();


    /**
     * <h1>rightTurn()</h1>
     * This method is used to invoke the treads on BinBot. Calling this
     * method will make BinBot's treads make a right turn.
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public void rightTurn();


    /**
     * <h1>stop()</h1>
     * This method is used to halt the treads on BinBot. Calling this method
     * will bring BinBot to a standstill by ceasing the treads
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public void stop();


}