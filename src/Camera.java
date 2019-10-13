public interface Camera{

    /**
     * <h1> capture_photo() </h1>
     * This method invokes the camera feature on BinBot taking
     * a photo of what is in front of its path
     *
     *
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    void capture_photo();


    /**
     * <h1>get_proximity()</h1>
     * This method is used to calculate the distance to an identified
     * object
     *
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    void get_proximity();


    /**
     * <h1>in_range()</h1>
     * This method is used to check if an identify waste object
     * is in range of BinBot's arm, if the waste is in range method
     * will return true otherwise it will return false
     *
     *
     *
     * @author Jose Silva
     * @version 1.0
     * @since 2019-10-13
     */
    public boolean in_range();



}